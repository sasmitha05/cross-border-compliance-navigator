from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.agent import evaluate_compliance
    from backend.explainer import generate_explanation
    from backend.schemas import ComplianceRequest
except ImportError as e:
    print(f"Import error: {e}")
    pass

class handler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
        
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response = {
            "status": "ok",
            "message": "API is running"
        }
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON
            data = json.loads(body)
            
            # Validate required fields
            required_fields = ['country_from', 'country_to', 'data_type', 'action_type']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate with Pydantic
            request_data = ComplianceRequest(**data)
            
            # Evaluate compliance
            result = evaluate_compliance(
                request_data.country_from,
                request_data.country_to,
                request_data.data_type,
                request_data.action_type
            )
            
            # Generate explanation
            explanation = generate_explanation(
                request_data.country_from,
                request_data.country_to,
                request_data.data_type,
                result["status"],
                result["risk_score"]
            )
            
            # Add explanation to result
            result["ai_explanation"] = explanation
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode())
            
        except json.JSONDecodeError as e:
            self._send_error(400, f"Invalid JSON: {str(e)}")
            
        except ValueError as e:
            self._send_error(400, str(e))
            
        except Exception as e:
            self._send_error(500, f"Server error: {str(e)}")
    
    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        error_response = {
            "status": "ERROR",
            "risk_score": 0,
            "ai_explanation": message
        }
        
        self.wfile.write(json.dumps(error_response).encode())