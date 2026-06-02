# main.py
# FastAPI application entry point

import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import all routers
from routes.auth_routes import router as auth_router
from routes.review_cycle_routes import router as cycle_router
from routes.goal_routes import router as goal_router
from routes.review_routes import router as review_router
from routes.manager_routes import router as manager_router
from routes.competency_routes import router as competency_router
from routes.admin_routes import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle"""
    print("=" * 55)
    print("🚀 Performance Review Portal API is starting...")
    print("=" * 55)

    try:
        from db import init_db
        init_db()
    except Exception as e:
        print(f"⚠️  DB Warning: {e}")

    print("✅ Swagger UI ready at: http://localhost:8000/docs")
    print("=" * 55)

    yield

    print("🛑 Shutting down API...")
    try:
        from db import close_pool
        close_pool()
    except Exception:
        pass


# Create app
app = FastAPI(
    title="AI-Powered Performance Review Portal",
    description="Backend API for employee performance reviews",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# ─── Global Exception Handler ──────────────────────────────────
# This catches ALL 500 errors and prints the real cause
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Shows the REAL error instead of just 500 Internal Server Error.
    This makes debugging much easier.
    """
    error_detail = traceback.format_exc()

    # Print to console so you can see it in terminal
    print("\n" + "=" * 60)
    print(f"❌ ERROR on {request.method} {request.url}")
    print("=" * 60)
    print(error_detail)
    print("=" * 60 + "\n")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "traceback": error_detail
        }
    )


# ─── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ─── Register Routers ──────────────────────────────────────────
app.include_router(auth_router)
app.include_router(cycle_router)
app.include_router(goal_router)
app.include_router(review_router)
app.include_router(manager_router)
app.include_router(competency_router)
app.include_router(admin_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "service": "Performance Review Portal API",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}