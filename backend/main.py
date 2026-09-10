from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "CareerBridge API",
    description = "Backend API for CareerBridge",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

#=========required skills for each role=========

role_skills = {
   
    "Ayurvedic Physician/Intern (BAMS)" : [
        "Ayurvedic diagnosis (Nidan)", 
        "Prakriti assessment, classical texts (Charaka/Sushruta Samhita)", 
        "pulse diagnosis (Nadi Pariksha)", 
        "prescription/formulation knowledge", 
        "patient counseling", 
        "clinical documentation"
    ],

    "Panchkarma Therapist" : [
        "Panchakarma procedures (Vamana, Virechana, Basti, Nasya, Raktamokshana)", 
        "Abhyanga & Swedana techniques",
        "herbal oil/medicine application",
        "patient safety protocols", 
        "pre/post-procedure care",
        "physical stamina"
    ],

    "Yoga Instructor" : [
        "Asana & Pranayama instruction",
        "Yoga therapy for specific conditions", 
        "anatomy & physiology basics", 
        "sequencing/class planning",
        "communication & demonstration skills", 
        "certification (Yoga Alliance/AYUSH-recognized)"
    ],

    "Herbal Quality Analyst" : [
        "Pharmacognosy",
        "phytochemical analysis",
        "HPLC/GC testing", 
        "quality control per API (Ayurvedic Pharmacopoeia of India) standards", 
        "raw material authentication",
        "lab documentation",
        "adulteration detection"
    ],

    "Ayurvedic Pharmacist" : [
        "Ayurvedic pharmaceutics (Bhaishajya Kalpana)",
        "formulation preparation (Churna, Asava-Arishta, Bhasma)", 
        "GMP compliance",
        "dispensing knowledge",
        "drug storage/stability", 
        "regulatory labeling"
    ],

    "Clinical Research Associate (Ayurveda)" : [
        "Clinical trial design (CTRI registration)",
        " GCP (Good Clinical Practice)",
        "data collection & biostatistics basics," 
        "protocol writing", 
        "ethics compliance", 
        "pharmacovigilance", 
        "report documentation"
    ],

    "Wellness Centre Manager" : [
        "Operations management, staff scheduling", 
        "customer/patient relations", 
        "basic finance & billing", 
        "marketing for wellness services", 
        "compliance with health & safety norms", 
        "inventory management"
    ],

    "Regulatory Affairs (AYUSH Compilance)" : [
        "AYUSH licensing procedures", 
        "Drugs & Cosmetics Act (Ayurveda provisions)", 
        "labeling/claims regulations", 
        "documentation for approvals", 
        "liaison with regulatory bodies", 
        "audit readiness"
    ]
}


# ============ Skill Matching =============

@app.post("/skill-gap")
def skill_gap(student: Student):
    required_skills = role_skills.get(student.target_role, [])

    matching_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in [s.lower() for s in student.skills]:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "message": "Skill gap analysis completed successfully",
        "student_name": student.name,
        "target_role": student.target_role,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }

#============ Internship Match Score =============

@app.post("/match-internship")
def match_internship(student: Student, internship: Internship):
    matching_skills = []
    missing_skills = []

    student_skills_lower = [skill.lower() for skill in student.skills]

    for skill in internship.skills_required:
        if skill.lower() in student_skills_lower:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)
    total_required = len(internship.skills_required)
    total_matching = len(matching_skills)

    match_score = (total_matching / total_required) * 100 if total_required > 0 else 0

    return {
        "student" : student.name,
        "internship" : internship.role,
        "match_score" : f"{match_score:.2f}",
        "matching skills" : matching_skills,
        "missing skills" : missing_skills
    }