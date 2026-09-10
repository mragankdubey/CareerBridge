from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title = "CarrerBridge API",
    description = "Backend API for CarrerBridge",
    version = "1.0.0"
)

class Student (BaseModel):
    name : str
    skills : list[str]
    domain : str
    target_role : str

class Industry (BaseModel):
    name : str
    industry : str

class Internship (BaseModel):
    industry : str
    role : str
    description : str
    skills_required : list[str]

class Academia (BaseModel):
    name : str
    institution_type : str
    
students = []
industries = []
internships = []
academia = []

# Home route to check if the API is running

@app.get("/")
def home():
    return {
        "message": "CareerBridge API is running successfully"
    }

# ============= Student =============

#Create a student profile

@app.post("/students")
def create_student(student: Student):
    students.append(student)
    return {
        "message": "Student Profile created successfully",
        "student": student
    }

# Get all student profiles

@app.get("/students")
def get_students():
    return {
        "message": "Students retrieved successfully",
        "students": students
    }

#============ Academia =============

# Create an Academia profile

@app.post("/academia")
def create_academia(academia_profile: Academia):
    academia.append(academia_profile)
    return {
        "message": "Academia Profile created successfully",
        "academia": academia_profile
    }

# Get all academia profiles

@app.get("/academia")
def get_academia():
    return {
        "message": "Academia profiles retrieved successfully",
        "academia": academia
    }

#============ Industry =============

# Create an Industry profile

@app.post("/industries")
def create_industry(industry: Industry):
    industries.append(industry)
    return {
        "message": "Industry Profile created successfully",
        "industry": industry
    }

# Get all industry profiles

@app.get("/industries")
def get_industries():
    return {
        "message": "Industries retrieved successfully",
        "industries": industries
    }

#============ Internship =============

@app.post("/internships")
def create_internship(internship: Internship):
    internships.append(internship)
    return {
        "message": "Internship created successfully",
        "internship": internship
    }

@app.get("/internships")
def get_internships():
    return {
        "message": "Internships retrieved successfully",
        "internships": internships
    }

