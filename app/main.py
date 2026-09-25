from fastapi import FastAPI

from app.database import engine, Base

from employee_routers.routers import router as employee_routers

# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Employee Record Management API",
    version="1.0.0"
)


# Register employee routes
app.include_router(employee_routers)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Employee Management API is running"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }