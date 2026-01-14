from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(resume_text, job_text, resume_skills, job_skills):
    # -------------------------------------------------
    # 1. DEFINE CRITICAL SKILLS (ATS RULE)
    # -------------------------------------------------
    # Treat all job skills as mandatory for now
    critical_skills = job_skills.copy()
    missing_critical_skills = list(set(critical_skills) - set(resume_skills))

    # -------------------------------------------------
    # 2. SKILL MATCH
    # -------------------------------------------------
    matched_skills = list(set(resume_skills).intersection(set(job_skills)))
    missing_skills = list(set(job_skills) - set(resume_skills))

    if not job_skills:
        skill_score = 0
    else:
        skill_score = len(matched_skills) / len(job_skills)

    skill_match_percent = round(skill_score * 100, 2)

    # -------------------------------------------------
    # 3. TEXT SIMILARITY (TF-IDF + COSINE)
    # -------------------------------------------------
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])
    text_score = cosine_similarity(vectors[0], vectors[1])[0][0]

    text_similarity_percent = round(text_score * 100, 2)

    # -------------------------------------------------
    # 4. FINAL WEIGHTED ATS SCORE
    # -------------------------------------------------
    final_score = round((0.7 * skill_score + 0.3 * text_score) * 100, 2)

    # -------------------------------------------------
    # 5. AUTO-REJECT + SMART ATS REASONS
    # -------------------------------------------------
    auto_reject = False
    reasons = []

    # 🚫 Mandatory skills gate
    if missing_critical_skills:
        auto_reject = True
        reasons.append(
            "Missing mandatory skills: " + ", ".join(missing_critical_skills)
        )

    # ⚠️ Low skill coverage
    if skill_match_percent < 50:
        reasons.append(
            f"Low skill match: only {len(matched_skills)} out of {len(job_skills)} required skills matched."
        )

    # ⚠️ Soft reject: contextual / responsibility mismatch
    if text_similarity_percent < 45:
        reasons.append(
            "Resume content does not strongly align with job responsibilities."
        )

    # Fallback (selected / near-fit)
    if not reasons:
        reasons.append("Profile matches job requirements reasonably well.")

    # -------------------------------------------------
    # 6. IMPROVEMENT ESTIMATION (ATS STYLE)
    # -------------------------------------------------
    improvement_estimate = min(30, len(missing_skills) * 5)

    # -------------------------------------------------
    # 7. EXPLANATION OBJECT
    # -------------------------------------------------
    explanation = {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "critical_missing": missing_critical_skills,
        "skill_match_percent": skill_match_percent,
        "text_similarity_percent": text_similarity_percent,
        "auto_reject": auto_reject,
        "reasons": reasons,
        "improvement_estimate": improvement_estimate
    }

    return final_score, explanation
