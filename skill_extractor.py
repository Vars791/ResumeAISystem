import spacy
import subprocess
import sys

# =====================================================
# SAFE spaCy MODEL LOADER (FIXES STREAMLIT CLOUD ERROR)
# =====================================================
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Auto-download model if missing (Streamlit Cloud safe)
        subprocess.check_call(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
        )
        return spacy.load("en_core_web_sm")

# Load NLP model safely
nlp = load_spacy_model()


# =====================================================
# SKILL DATABASE (Expandable)
# =====================================================
SKILLS = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "data science",
    "nlp", "deep learning",
    "excel", "power bi", "tableau"
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
