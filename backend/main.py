from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import StudentDB, AcademiaDB, IndustryDB, InternshipDB, CourseDB
from sqlalchemy.orm import Session
from matching import calculate_skill_match
from course_matching import calculate_course_relevance

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

class Course(BaseModel):
    title: str
    provider: str
    description: str
    skills_taught: list[str]
    course_url: str

# Home route to check if the API is running

@app.get("/")
def home():
    return {
        "message": "CareerBridge API is running successfully"
    }

# ============= Student =============

#Create a student profile

@app.post("/students")
def create_student(student: Student,db: Session = Depends(get_db)):

    db_student = StudentDB(
        name=student.name,
        domain=student.domain,
        target_role=student.target_role,
        skills=", ".join(student.skills)
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return {
        "message": "Student Profile created successfully",
        "student": db_student
    }

# Get all student profiles

@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    students = db.query(StudentDB).all()

    return {
        "message": "Students retrieved successfully",
        "students": students
    }

#============ Academia =============

# Create an Academia profile

@app.post("/academia")
def create_academia(
    academia_profile: Academia,
    db: Session = Depends(get_db)
):

    db_academia = AcademiaDB(
        name=academia_profile.name,
        institution_type=academia_profile.institution_type
    )

    db.add(db_academia)
    db.commit()
    db.refresh(db_academia)


    return {
        "message": "Academia Profile created successfully",
        "academia": academia_profile
    }

# Get all academia profiles

@app.get("/academia")
def get_academia(db: Session = Depends(get_db)):

    academia_profiles = db.query(AcademiaDB).all()

    return {
        "message": "Academia profiles retrieved successfully",
        "academia": academia_profiles
    }

#============ Industry =============

# Create an Industry profile

@app.post("/industries")
def create_industry(
    industry: Industry,
    db: Session = Depends(get_db)
):

    db_industry = IndustryDB(
        name=industry.name,
        industry=industry.industry
    )

    db.add(db_industry)
    db.commit()
    db.refresh(db_industry)

    return {
        "message": "Industry Profile created successfully",
        "industry": db_industry
    }

# Get all industry profiles

@app.get("/industries")
def get_industries(db: Session = Depends(get_db)):

    industries = db.query(IndustryDB).all()

    return {
        "message": "Industries retrieved successfully",
        "industries": industries
    }

#============ Internship =============

@app.post("/internships")
def create_internship(
    internship: Internship,
    db: Session = Depends(get_db)
):

    db_internship = InternshipDB(
        industry=internship.industry,
        role=internship.role,
        description=internship.description,
        skills_required=", ".join(internship.skills_required)
    )

    db.add(db_internship)
    db.commit()
    db.refresh(db_internship)

    return {
        "message": "Internship created successfully",
        "internship": {
            "id": db_internship.id,
            "industry": db_internship.industry,
            "role": db_internship.role,
            "description": db_internship.description,
            "skills_required": db_internship.skills_required
        }
    }


@app.get("/internships")
def get_internships(db: Session = Depends(get_db)):

    internships = db.query(InternshipDB).all()

    return {
        "message": "Internships retrieved successfully",
        "internships": internships
    }

#=========courses==========

@app.post("/courses")
def create_course(
    course: Course,
    db: Session = Depends(get_db)
):

    db_course = CourseDB(
        title=course.title,
        provider=course.provider,
        description=course.description,
        skills_taught=", ".join(course.skills_taught),
        course_url=course.course_url
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return {
        "message": "Course created successfully",
        "course": {
            "id": db_course.id,
            "title": db_course.title,
            "provider": db_course.provider,
            "description": db_course.description,
            "skills_taught": db_course.skills_taught,
            "course_url": db_course.course_url
        }
    }


@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):

    courses = db.query(CourseDB).all()

    return {
        "message": "Courses retrieved successfully",
        "courses": courses
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

    result = calculate_skill_match(
        student.skills,
        required_skills
    )

    return {
        "message": "Skill gap analysis completed successfully",
        "student_name": student.name,
        "target_role": student.target_role,
        "matching_skills": result["matching_skills"],
        "missing_skills": result["missing_skills"],
        "match_score": result["match_score"]
    }

#============ Internship Match Score =============

@app.get("/students/{student_id}/matches")
def get_internship_matches(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Find Student
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()
    if not student:
        return {
            "message": "Student not found"
        }

    # Get all internship
    internships = db.query(InternshipDB).all()
    results = []

    # Student skills into list
    student_skills = [
        skill.strip()
        for skill in student.skills.split(",")
    ]

    # Compare student with all internships
    for internship in internships:
        required_skills = [
            skill.strip()
            for skill in internship.skills_required.split(",")
        ]
        result = calculate_skill_match(
            student_skills,
            required_skills
        )
        results.append({
            "internship_id": internship.id,
            "industry": internship.industry,
            "role": internship.role,
            "description": internship.description,
            "match_score": result["match_score"],
            "matching_skills": result["matching_skills"],
            "missing_skills": result["missing_skills"]
        })

    # Highest to lowest match
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "student_id": student.id,
        "student_name": student.name,
        "matches": results
    }

#===========Course Recommendation===========

@app.get("/students/{student_id}/course-recommendations")
def get_course_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):

    #Find Student
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()
    if not student:
        return {
            "message": "Student not found"
        }

    # Req skills for student's targeting role
    required_skills = role_skills.get(
        student.target_role,
        []
    )

    #Student's skills into list
    student_skills = [
        skill.strip()
        for skill in student.skills.split(",")
    ]

    #Find missing skills
    skill_gap = calculate_skill_match(
        student_skills,
        required_skills
    )
    missing_skills = skill_gap["missing_skills"]

    # All courses
    courses = db.query(CourseDB).all()

    recommendations = []

    # Compare course with missing skills
    for course in courses:
        course_skills = [
            skill.strip()
            for skill in course.skills_taught.split(",")
        ]

        result = calculate_course_relevance(
            missing_skills,
            course_skills
        )

        # Only recommend courses that cover at least one missing skill
        if result["relevance_score"] > 0:

            recommendations.append({
                "course_id": course.id,
                "title": course.title,
                "provider": course.provider,
                "description": course.description,
                "course_url": course.course_url,
                "relevance_score": result["relevance_score"],
                "matching_skills": result["matching_skills"]
            })

    #High relevance to Low
    recommendations.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    return {
        "student_id": student.id,
        "student_name": student.name,
        "target_role": student.target_role,
        "missing_skills": missing_skills,
        "course_recommendations": recommendations
    }