from pydantic import BaseModel

class ComplianceRequest(BaseModel):
    country_from: str
    country_to: str
    data_type: str
    action_type: str   # new field
