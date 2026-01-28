from backend.agent import evaluate_compliance
from backend.explainer import generate_explanation
from backend.logger import log_decision
from backend.schemas import ComplianceRequest
import json

def handler(request):
    # CORS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Method not allowed"})
        }

    try:
        body = json.loads(request.body)
        data = ComplianceRequest(**body)

        result = evaluate_compliance(
            data.country_from,
            data.country_to,
            data.data_type,
            data.action_type
        )

        explanation = generate_explanation(
            data.country_from,
            data.country_to,
            data.data_type,
            result["status"],
            result["risk_score"]
        )

        log_decision(
            data.country_from,
            data.country_to,
            data.data_type,
            result["status"]
        )

        result["ai_explanation"] = explanation

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
