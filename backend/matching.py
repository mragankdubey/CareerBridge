def calculate_skill_match(student_skills, required_skills):

    matching_skills = []
    missing_skills = []

    student_skills_lower = [
        skill.lower().strip()
        for skill in student_skills
    ]

    for skill in required_skills:

        if skill.lower().strip() in student_skills_lower:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_required = len(required_skills)
    total_matching = len(matching_skills)

    match_score = (
        (total_matching / total_required) * 100
        if total_required > 0
        else 0
    )

    return {
        "match_score": round(match_score, 2),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }