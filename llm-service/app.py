from flask import Flask, request, jsonify, Response
import ollama
import time
import logging
import os
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://ollama:11434')
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

# Initialize Ollama client with retry logic
def get_ollama_client():
    client = None
    for attempt in range(MAX_RETRIES):
        try:
            client = ollama.Client(host=OLLAMA_HOST, timeout=60)
            # Test connection
            client.list()
            return client
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} - Failed to connect to Ollama: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    raise Exception(f"Failed to connect to Ollama after {MAX_RETRIES} attempts")

# Initialize client
client = None
try:
    client = get_ollama_client()
    logger.info("Successfully connected to Ollama service")
except Exception as e:
    logger.error(f"Initial connection to Ollama failed: {str(e)}")
    logger.warning("Will attempt to reconnect on first request")

def retry_on_failure(max_retries=3, delay=5, reconnect_ollama=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            global client
            last_exception = None
            for attempt in range(max_retries):
                try:
                    # Reconnect to Ollama if needed
                    if reconnect_ollama and (client is None or attempt > 0):
                        logger.info(f"Reconnecting to Ollama (attempt {attempt + 1})")
                        try:
                            client = get_ollama_client()
                        except Exception as e:
                            logger.error(f"Failed to reconnect to Ollama: {str(e)}")
                            if attempt == max_retries - 1:
                                raise
                            time.sleep(delay)
                            continue
                    
                    return f(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            
            logger.error(f"All {max_retries} attempts failed")
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure(max_retries=5, delay=5)
def check_and_pull_model():
    try:
        models = client.list()['models']
        if not any(model['name'] == 'gemma:2b' for model in models):
            logger.info("gemma:2b model not found, pulling...")
            client.pull('gemma:2b')
            logger.info("Model pulled successfully.")
    except Exception as e:
        logger.error(f"Failed to check/pull model: {str(e)}")
        raise

# Initialize model on startup
check_and_pull_model()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker healthcheck"""
    try:
        # Check if Ollama is responding
        if client is None:
            raise Exception("Ollama client not initialized")
            
        models = client.list()
        gemma_available = any('gemma:2b' in model.get('name', '') for model in models.get('models', []))
        
        if not gemma_available:
            logger.warning("Gemma 2B model not found in Ollama")
            return jsonify({
                "status": "degraded",
                "message": "Gemma 2B model not loaded",
                "available_models": [m['name'] for m in models.get('models', [])]
            }), 200
            
        return jsonify({
            "status": "healthy",
            "model": "gemma:2b",
            "ollama_status": "connected"
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "ollama_status": "disconnected"
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat completion requests"""
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data['prompt']
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Prompt must be a non-empty string"}), 400

    try:
        response = client.chat(
            model='gemma:2b',
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'temperature': data.get('temperature', 0.7),
                'top_p': data.get('top_p', 0.9),
                'max_tokens': data.get('max_tokens', 1000)
            }
        )
        return jsonify({
            'response': response['message']['content'],
            'model': 'gemma:2b',
            'usage': {
                'prompt_tokens': len(prompt.split()),
                'completion_tokens': len(response['message']['content'].split())
            }
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to process your request",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
