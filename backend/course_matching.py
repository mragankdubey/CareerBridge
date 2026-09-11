def calculate_course_relevance(missing_skills, course_skills):

    matching_skills = []

    missing_skills_lower = [
        skill.lower().strip()
        for skill in missing_skills
    ]

    for skill in course_skills:

        if skill.lower().strip() in missing_skills_lower:
            matching_skills.append(skill)

    total_missing = len(missing_skills)
    total_matching = len(matching_skills)

    relevance_score = (
        (total_matching / total_missing) * 100
        if total_missing > 0
        else 0
    )

    return {
        "relevance_score": round(relevance_score, 2),
        "matching_skills": matching_skills
    }