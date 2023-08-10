from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import create_students_table, table_exists, insert_student, get_students, delete_student
from routers.routers_admin import router as admin_router  # Update the import path


app = FastAPI()

@app.get("/")
def redroot():
    return {"Hello": "To the application"}

# Include the admin router in the app
app.include_router(admin_router, prefix="/admin", tags=["admin"])
