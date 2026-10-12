from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, chatbot, resume, roadmap, interview, dsa

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Modular Routers under /api
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(resume.router, prefix="/api/resume", tags=["Resume Generator"])
app.include_router(roadmap.router, prefix="/api/roadmap", tags=["Roadmap Generator"])
app.include_router(interview.router, prefix="/api/interview", tags=["Mock Interview"])
app.include_router(dsa.router, prefix="/api/dsa", tags=["Technical DSA"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}!",
        "health": "/api/health",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.PORT, reload=True)
