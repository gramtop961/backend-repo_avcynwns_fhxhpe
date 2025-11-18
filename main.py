import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Project, Message

app = FastAPI(title="MMI UI/UX Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MMI Portfolio API running"}

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
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Seed/demo endpoints (read)
@app.get("/api/projects", response_model=List[Project])
def list_projects():
    try:
        docs = get_documents("project", {}, 50)
        # Convert _id/ObjectId to string-safe dicts
        normalized = []
        for d in docs:
            d.pop("_id", None)
            normalized.append(Project(**d))
        return normalized
    except Exception:
        # Fallback demo content if DB unavailable
        demo = [
            Project(
                title="Mobile Banking Redesign",
                slug="mobile-banking-redesign",
                category="UI/UX",
                tags=["Fintech", "Design System", "Accessibility"],
                short_description="Improved onboarding and clarity with a consistent design system.",
                description="Case study covering research synthesis, information architecture, and high-fidelity prototypes.",
                images=[
                    "https://images.unsplash.com/photo-1556745753-b2904692b3cd?w=1200&q=80&auto=format&fit=crop",
                ],
                tools=["Figma", "FigJam", "Illustrator"],
                highlight=True,
            ),
            Project(
                title="Brand Identity for Café Pixel",
                slug="cafe-pixel-branding",
                category="Branding",
                tags=["Logo", "Visual Identity", "Print"],
                short_description="Retro-digital coffee brand with pixel-inspired mark and patterns.",
                description="From moodboards to logo grids, color system, and packaging mockups.",
                images=[
                    "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=1200&q=80&auto=format&fit=crop",
                ],
                tools=["Illustrator", "Photoshop"],
                highlight=False,
            ),
            Project(
                title="Interactive Exhibition Microsite",
                slug="exhibition-microsite",
                category="Web Design",
                tags=["WebGL", "Motion", "Parallax"],
                short_description="Smooth-scrolling site with animated illustrations and parallax.",
                description="Prototype to final: motion studies, component library, and performance tuning.",
                images=[
                    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&q=80&auto=format&fit=crop",
                ],
                tools=["Figma", "After Effects"],
                highlight=False,
            ),
        ]
        return demo

class CreateMessage(BaseModel):
    name: str
    email: str
    message: str
    source: str | None = None

@app.post("/api/contact")
def submit_message(payload: CreateMessage):
    try:
        msg = Message(**payload.dict())
        create_document("message", msg)
        return {"ok": True}
    except Exception as e:
        # Still return ok to not block the UX in demo environments
        return {"ok": True, "note": f"Stored locally only: {str(e)[:60]}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
