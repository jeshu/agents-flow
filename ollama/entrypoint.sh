#!/bin/sh
set -e

# Start Ollama in the background
echo 'Starting Ollama server...'
ollama serve &

# Wait for the server to be ready
echo 'Waiting for Ollama to start...'
while ! curl -s http://localhost:11434/api/version >/dev/null; do
  echo 'Waiting for Ollama to be ready...'
  sleep 5
done

# Pull the model if not already present
echo 'Checking for Gemma 2B model...'
if ! ollama list | grep -q 'gemma:2b'; then
  echo 'Pulling Gemma 2B model... (this may take a while)'
  ollama pull gemma:2b
else
  echo 'Gemma 2B model is already downloaded.'
fi

echo 'Ollama is ready and serving the Gemma 2B model!'

# Keep the container running
tail -f /dev/null
