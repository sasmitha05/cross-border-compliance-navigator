from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.agent import evaluate_compliance
from backend.schemas import ComplianceRequest
from backend.regulation_state import REGULATION_STATE, save_state

app = FastAPI(title="Cross-Border Compliance Navigator")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compliance check endpoint
@app.post("/api/check_compliance")
def check_compliance(payload: ComplianceRequest):
    try:
        return evaluate_compliance(
            payload.country_from,
            payload.country_to,
            payload.data_type,
            payload.action_type
        )
    except Exception as e:
        return {
            "status": "ERROR",
            "risk_score": 0,
            "ai_explanation": f"Internal Server Error: {str(e)}"
        }

# Dynamic simulation endpoint
@app.post("/api/simulate-regulation-update")
async def simulate_regulation_update(request: Request):
    try:
        payload = await request.json()
        action_to_block = payload.get("action_to_block", "share_customer_data")

        india_rules = REGULATION_STATE.get("India", {})
        india_rules["allowed_actions"] = india_rules.get("allowed_actions", [
            "share_customer_data",
            "export_financial_data",
            "access_internal_system"
        ])

        if action_to_block in india_rules["allowed_actions"]:
            india_rules["allowed_actions"].remove(action_to_block)

        REGULATION_STATE["India"] = india_rules
        save_state(REGULATION_STATE)

        return {
            "message": "🚨 Regulation updated",
            "country": "India",
            "impact": f"Action '{action_to_block}' is now BLOCKED for cross-border transfer"
        }
    except Exception as e:
        return {"message": "Internal Server Error", "error": str(e)}

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
