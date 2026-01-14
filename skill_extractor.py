import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Skill database (can be expanded later)
SKILLS = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "data science",
    "nlp", "deep learning",
    "excel", "power bi", "tableau"
]

# --------- Extract skills from RESUME ---------
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# --------- Extract skills from JOB DESCRIPTION ---------
def extract_skills_from_job(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
