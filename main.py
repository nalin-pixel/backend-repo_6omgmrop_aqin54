import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents
from schemas import Lead

app = FastAPI(title="VD Pulizie API", description="API per la raccolta lead e preventivi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "VD Pulizie Backend attivo"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Request model for lead creation (frontend-friendly)
class LeadRequest(BaseModel):
    name: str
    email: str
    phone: str
    service_type: str
    square_meters: int | None = None
    frequency: str | None = None
    message: str | None = None

@app.post("/api/leads")
def create_lead(lead: LeadRequest):
    try:
        # Validate with Pydantic schema and save
        lead_doc = Lead(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            service_type=lead.service_type,
            square_meters=lead.square_meters,
            frequency=lead.frequency,
            message=lead.message,
            source="website",
            status="nuovo"
        )
        lead_id = create_document("lead", lead_doc)
        return {"success": True, "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leads", response_model=List[dict])
def list_leads():
    try:
        items = get_documents("lead", {}, limit=50)
        # Convert ObjectId to string for JSON
        for it in items:
            if "_id" in it:
                it["_id"] = str(it["_id"]) 
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
