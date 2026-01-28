from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.agent import evaluate_compliance
from backend.explainer import generate_explanation
from backend.logger import log_decision
from backend.schemas import ComplianceRequest

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)
        self.wfile.write(b'')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
            # Validate request
            data = ComplianceRequest(**body)
            
            # Evaluate compliance
            result = evaluate_compliance(
                data.country_from,
                data.country_to,
                data.data_type,
                data.action_type
            )
            
            # Generate explanation
            explanation = generate_explanation(
                data.country_from,
                data.country_to,
                data.data_type,
                result["status"],
                result["risk_score"]
            )
            
            # Log decision
            log_decision(
                data.country_from,
                data.country_to,
                data.data_type,
                result["status"]
            )
            
            result["ai_explanation"] = explanation
            
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self._set_headers(500)
            error_response = {
                "status": "ERROR",
                "risk_score": 0,
                "ai_explanation": f"Server error: {str(e)}"
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))