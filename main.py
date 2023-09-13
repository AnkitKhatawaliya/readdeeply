from fastapi import FastAPI
from routers.routers_admin import router as admin_router
from routers.routers_teachers import router as teacher_router
from routers.routers_students import router as student_router
from routers.routers_parents import router as parent_router
from routers.routers_payment import router as payment_router
app = FastAPI()

@app.get("/")
def redroot():
    return {"Hello": "To the application"}

@app.get("/second")
def sed():
    return {"This": "is second dummy route"}

# Include the admin router in the app
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(teacher_router ,prefix="/teacher", tags=["teacher"])
app.include_router(student_router ,prefix="/student", tags=["student"])
app.include_router(parent_router , prefix="/parent", tags=["parent"])
app.include_router(payment_router, prefix="/payment", tags=["payment"])
