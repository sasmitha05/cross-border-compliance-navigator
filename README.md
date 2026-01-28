# 🌍 Cross-Border Compliance Navigator

A rule-based compliance analysis system that evaluates **cross-border data transfer requests** using country-specific regulations, risk scoring, and AI-style explanations.

This project helps organizations quickly determine whether a proposed international data transfer is **ALLOWED**, **BLOCKED**, or **REQUIRES REVIEW**, based on simulated regulatory policies such as GDPR and national data laws.



## 🚀 Features

* 🌐 **Country-aware regulation engine**
* 📊 **Risk scoring (0–100)** based on data type and destination
* 🧠 **Human-readable AI explanations** for compliance decisions
* 🔄 **Dynamic regulation updates** (simulated law changes)
* 📝 **Audit logging** for traceability
* 🖥️ **Clean web UI** for interactive compliance checks



## 🧠 How It Works (High-Level)

1. User submits a compliance request:

   * Source country
   * Destination country
   * Data type (personal / financial / non-personal)
   * Action type (share, export, access)

2. The system:

   * Validates against country-specific rules
   * Calculates a risk score
   * Applies destination-based regulations (e.g., GDPR)
   * Generates an explainable decision

3. Output:

   * **Status**: `ALLOWED`, `REVIEW_REQUIRED`, or `BLOCKED`
   * **Risk Score**
   * **AI-style Explanation**


## 🏗️ Project Architecture

```text
cross-border-compliance-navigator/
│
├── backend/
│   ├── agent.py                # Core compliance evaluation logic
│   ├── regulation_state.py    # Loads & persists regulation state
│   ├── regulation_agent.py    # Simulates regulation updates
│   ├── explainer.py            # Generates AI-style explanations
│   ├── logger.py               # Compliance decision logging
│   ├── schemas.py              # Pydantic request schema
│   ├── rules.json              # Country-level allowed data/actions
│   ├── regulation_state.json  # Dynamic regulation decisions
│   └── audit_logs.json         # Sample audit history
│
├── frontend/
│   └── index.html              # Interactive compliance UI
│
├── main.py                     # API entry point
└── README.md



## ⚙️ Core Logic Explained

### 🔍 Compliance Evaluation

Implemented in `backend/agent.py`

The system checks:

* Whether the source country exists
* If the data type is allowed
* If the requested action is permitted

Then computes a **risk score**:

* Base risk: `20`
* Personal data: `+50`
* GDPR destination (EU, Germany, France): `+20`

```python
status = "ALLOWED" if risk_score < 80 else "REVIEW_REQUIRED"
```

If rules are violated → `BLOCKED` with risk `100`.


### 🧠 AI-Style Explanation Engine

Implemented in `backend/explainer.py`

Generates a natural-language explanation covering:

* Origin & destination
* Data sensitivity
* Regulatory impact (e.g., GDPR)
* Final compliance outcome
* Risk score

This makes decisions **transparent and audit-friendly**.


### 🔄 Regulation Update Simulation

Implemented in `backend/regulation_agent.py`

Simulates sudden regulatory changes, such as:

```json
"India": {
  "share_customer_data": {
    "risk": "HIGH",
    "rule": "New Indian data law requires strict localization",
    "decision": "BLOCK"
  }
}
```

This mimics **real-world regulatory volatility**.

### 📝 Audit Logging

Implemented in `backend/logger.py`

Each decision is logged with:

* Timestamp
* Source → Destination
* Data type
* Final status

Useful for:

* Compliance audits
* Historical tracking
* Explainability


## 🖥️ Frontend UI

The frontend (`frontend/index.html`) provides:

* Clean, responsive UI
* Country & data selectors
* Real-time compliance result
* Visual risk indicators:

  * ✅ Allowed
  * ⚠️ Review Required
  * 🚫 Blocked

The UI communicates with the backend via:

```
POST /api/check-compliance
```

---

## 📦 Example API Request

```json
{
  "country_from": "India",
  "country_to": "Germany",
  "data_type": "personal_data",
  "action_type": "share_customer_data"
}
```

### Example Response

```json
{
  "status": "BLOCKED",
  "risk_score": 100,
  "ai_explanation": "GDPR requires explicit consent before exporting personal data..."
}
```

## 🧪 Use Cases

* Compliance pre-check for SaaS platforms
* Internal data governance tools
* Legal & risk assessment simulations
* Hackathons & academic demonstrations

## ⚠️ Disclaimer

This project **simulates** regulatory logic for educational and demonstrative purposes.
It is **not legal advice** and should not be used as a substitute for professional compliance review.

