from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/servers')
def get_servers():
    servers = [
        {"id": 1, "name": "MCP Server 1", "status": "online"},
        {"id": 2, "name": "MCP Server 2", "status": "offline"},
        {"id": 3, "name": "MCP Server 3", "status": "online"}
    ]
    return jsonify(servers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

