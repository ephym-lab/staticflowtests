import asyncio
from os import environ
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Import StaticFlow components
from staticfloww import Gateway, StaticPayload, MemoryAuditor
from utils import inject_lapfund_creds

# 1. Load your .env file so os.environ can see BASE_URL
load_dotenv()

app = Flask(__name__)

# 2. Initialize Auditor and Gateway
# We use a fallback URL just in case the .env isn't found
auditor = MemoryAuditor()
base_url = environ.get("BASE_URL") or "https://mssadmin.lapfund.or.ke"
gateway = Gateway(base_url=base_url, auditor=auditor)

# 3. Register External Routes (Lapfund)
gateway.add_route(
    action="GET_TOKEN",           
    path="/connect/token",        
    method="POST",
    before_request=inject_lapfund_creds,
    request_format="form"  # Ensures application/x-www-form-urlencoded
)

# 4. Register Internal Routes (Self-pointing for logs)
gateway.add_route(
    action="GET_LOGS",
    base_url="http://localhost:5000", # Point to your own Flask server
    path="/logs",
    method="GET"
)

@app.route('/gateway/process', methods=['POST'])
def process_flow():
    """
    The main 'God Schema' entry point.
    Routes every request based on the 'action' field.
    """
    raw_payload = request.get_json()
    
    try:
        # Convert raw JSON to StaticPayload (validation happens here)
        payload = StaticPayload(**raw_payload)
        
        # Execute the request through the gateway
        result = asyncio.run(gateway.route_request(
            payload=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        ))
        return jsonify(result)
    except Exception as e:
        # StaticFlow 0.1.8+ captures tracebacks automatically in the auditor!
        return jsonify({"error": str(e)}), 500

@app.route('/logs', methods=['GET'])
def logs():
    """
    Internal endpoint to view real-time audit logs.
    """
    try:
        # MemoryAuditor returns the structured history
        history = asyncio.run(auditor.get_logs(limit=20))
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure your Flask port matches the GET_LOGS base_url above
    app.run(host="localhost", port=5000, debug=True)
