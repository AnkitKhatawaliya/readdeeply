from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.routers_admin import router as admin_router

app = FastAPI()

@app.get("/")
def redroot():
    return {"Hello": "To the application"}

@app.get("/second")
def sed():
    return {"This": "is second dummy route"}

# Include the admin router in the app
app.include_router(admin_router, prefix="/admin", tags=["admin"])
