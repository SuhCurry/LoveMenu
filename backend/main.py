"""
LoveMenu Backend - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import dishes, orders

# Initialize FastAPI app
app = FastAPI(
    title="LoveMenu API",
    description="A personal food ordering system for couples",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
# In production, specify frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dishes.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on startup
    """
    init_db()
    print("Database initialized")


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {
        "message": "LoveMenu API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


