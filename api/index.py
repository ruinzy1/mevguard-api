from flask import Flask, jsonify, request

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

# --- 1. HALAMAN UTAMA (HTML) ---
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MEVGuard AI Agent</title>
        <style>
            body {
                background-color: #0d1117; color: #c9d1d9;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                display: flex; justify-content: center; align-items: center;
                height: 100vh; margin: 0;
            }
            .container {
                text-align: center; padding: 50px; border: 1px solid #30363d;
                border-radius: 15px; background-color: #161b22;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5); max-width: 500px;
            }
            h1 { color: #58a6ff; margin-bottom: 10px; }
            p { font-size: 16px; line-height: 1.5; color: #8b949e; margin-bottom: 30px; }
            .status-badge {
                padding: 8px 16px; background-color: #238636; color: #ffffff;
                border-radius: 20px; font-size: 14px; font-weight: bold;
                display: inline-block; border: 1px solid #2ea043;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MEVGuard AI</h1>
            <p>Advanced MEV protection and intent-solving agent. Shields user transactions from front-running, optimizes cross-chain liquidity routing, and executes private mempool transactions on the Base network.</p>
            <div class="status-badge">🟢 System Online & Healthy</div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- 2. ENDPOINT MCP ---
@app.route('/mcp', methods=['GET', 'POST', 'OPTIONS'])
def mcp_endpoint():
    server_info = {
        "name": "MEVGuard Agent Server",
        "version": "1.0.0",
        "website": "https://mevguard-api.vercel.app",
        "description": "MEV protection and transaction routing agent"
    }
    tools = [
        {"name": "detect_sandwich_attack", "description": "Analyze mempool for pending sandwich attacks", "inputSchema": {"type": "object","properties": {}}},
        {"name": "route_private_tx", "description": "Route transaction through private RPC endpoints", "inputSchema": {"type": "object","properties": {}}},
        {"name": "optimize_slippage", "description": "Calculate dynamic slippage tolerance for large swaps", "inputSchema": {"type": "object","properties": {}}}
    ]
    prompts = [
        {"name": "mev_exposure_report", "description": "Report on potential MEV value extraction for a token", "arguments": []},
        {"name": "intent_execution_plan", "description": "Generate optimal routing path for user intent", "arguments": []}
    ]
    
    if request.method == 'GET':
        return jsonify({
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "tools": tools,
            "prompts": prompts,
            "resources": [] 
        })

    req_data = request.get_json(silent=True) or {}
    req_id = req_data.get("id", 1)
    method = req_data.get("method", "")

    if method == "tools/list":
        result = {"tools": tools}
    elif method == "prompts/list":
        result = {"prompts": prompts}
    else:
        result = {
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "capabilities": {"tools": {},"prompts": {},"resources": {}}
        }

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

# --- 3. ENDPOINT A2A (ID AKUN 12: 22383) ---
@app.route('/.well-known/agent-card.json', methods=['GET','OPTIONS'])
def a2a_endpoint():
    return jsonify({
        "id": "mevguard",
        "name": "mevguard",
        "version": "1.0.0",
        "description": "Advanced MEV protection and intent-solving agent.",
        "website": "https://mevguard-api.vercel.app",
        "url": "https://mevguard-api.vercel.app",
        "documentation_url": "https://mevguard-api.vercel.app",
        "provider": {
            "organization": "MEVGuard Solutions",
            "url": "https://mevguard-api.vercel.app"
        },
        "registrations": [
            {
                "agentId": 22383,
                "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
            }
        ],
        "supportedTrust": ["reputation", "tee-attestation"],
        "skills": [
            {"name": "MEV Protection", "description": "Block sandwich attacks", "category": "security/mev_protection"},
            {"name": "Liquidity Routing", "description": "Find best swap paths", "category": "market/liquidity_routing"},
            {"name": "Tx Optimization", "description": "Manage dynamic slippage", "category": "technology/transaction_optimization"}
        ]
    })

# --- 4. ENDPOINT OASF ---
@app.route('/oasf', methods=['GET','OPTIONS'])
def oasf_endpoint():
    return jsonify({
        "id": "mevguard",
        "name": "mevguard",
        "version": "v0.8.0",
        "description": "Main endpoint for MEVGuard AI",
        "website": "https://mevguard-api.vercel.app",
        "protocols": ["mcp","a2a"],
        "capabilities": ["detect_sandwich_attack", "route_private_tx", "optimize_slippage"],
        "skills": [
            {"name": "security/mev_protection","type": "analytical"},
            {"name": "market/liquidity_routing","type": "operational"},
            {"name": "technology/transaction_optimization","type": "analytical"}
        ],
        "domains": [
            "web3/defi",
            "technology/mempool",
            "security/transaction_privacy"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
