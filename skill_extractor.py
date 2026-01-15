# skill_extractor.py
import spacy

# =====================================================
# SAFE spaCy LOADER (STREAMLIT CLOUD COMPATIBLE)
# =====================================================
def load_nlp():
    try:
        # Works locally if model is installed
        return spacy.load("en_core_web_sm")
    except Exception:
        # Streamlit Cloud fallback (NO downloads)
        return spacy.blank("en")

nlp = load_nlp()

# =====================================================
# SKILL DATABASE (Internship-friendly)
# =====================================================
SKILLS = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "data science",
    "nlp", "deep learning",
    "excel", "power bi", "tableau",
    "streamlit", "pandas", "numpy"
]

# =====================================================
# EXTRACT SKILLS FROM RESUME
# =====================================================
def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# =====================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# =====================================================
def extract_skills_from_job(text):
    if not text:
        return []

    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
