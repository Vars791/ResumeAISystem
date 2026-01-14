from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills, extract_skills_from_job
from matcher import calculate_match
from llmanalyzer import llmanalysis   # STEP 4: AI HR feedback
from interviewquestions import generateInterviewQuestions   # STEP 6


# =====================================================
# STEP 3 — RESUME IMPROVEMENT ROADMAP BUILDER
# =====================================================
def build_improvement_roadmap(missing_skills, reasons, improvement_estimate):
    roadmap = []

    if missing_skills:
        roadmap.append("🔴 Priority Skills to Learn:")
        for idx, skill in enumerate(missing_skills, start=1):
            roadmap.append(f"{idx}. Learn {skill} (basics + small projects)")
    else:
        roadmap.append("🟢 Skills are mostly aligned with the role.")

    roadmap.append("📝 Resume Improvements:")
    roadmap.append("• Add missing keywords from job description")
    roadmap.append("• Include 1–2 role-specific projects")
    roadmap.append("• Quantify achievements (numbers, impact)")
    roadmap.append("• Improve summary to match job role")

    if reasons:
        roadmap.append("❓ Address These Issues:")
        for reason in reasons:
            roadmap.append(f"• {reason}")

    estimated_days = max(7, len(missing_skills) * 5)
    roadmap.append(f"⏱️ Estimated Improvement Time: {estimated_days} days")
    roadmap.append(f"📈 Expected ATS Score Increase: ~{improvement_estimate}%")

    return roadmap


# =====================================================
# MAIN RANKING FUNCTION
# =====================================================
def rank_resumes(resume_files, job_text):
    results = []

    job_skills = extract_skills_from_job(job_text) or []

    for resume_file in resume_files:
        resume_text = extract_text_from_pdf(resume_file)
        resume_skills = extract_skills(resume_text)

        score, explanation = calculate_match(
            resume_text,
            job_text,
            resume_skills,
            job_skills
        )

        matched_skills = explanation.get("matched_skills", [])
        missing_skills = explanation.get("missing_skills", [])
        reasons = explanation.get("reasons", [])
        improvement_estimate = explanation.get("improvement_estimate", 0)
        skill_match_percent = explanation.get("skill_match_percent", 0)

        # -------------------------------------------------
        # 🚫 AUTO-REJECT LOGIC
        # -------------------------------------------------
        auto_reject = False

        if skill_match_percent < 30:
            auto_reject = True

        if job_skills and len(missing_skills) >= len(job_skills) * 0.6:
            auto_reject = True

        # -------------------------------------------------
        # STEP 3 — RESUME IMPROVEMENT ROADMAP
        # -------------------------------------------------
        roadmap = build_improvement_roadmap(
            missing_skills,
            reasons,
            improvement_estimate
        )

        # -------------------------------------------------
        # STEP 4 — AI HR FEEDBACK
        # -------------------------------------------------
        feedback = llmanalysis(
            score,
            matched_skills,
            missing_skills
        )

        # -------------------------------------------------
        # STEP 6 — AI INTERVIEW QUESTIONS
        # -------------------------------------------------
        interview_questions = generateInterviewQuestions(
            matched_skills,
            missing_skills
        )

        # -------------------------------------------------
        # FINAL RESULT OBJECT
        # -------------------------------------------------
        results.append({
            "name": resume_file.name,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "reasons": reasons,
            "improvement_estimate": improvement_estimate,
            "auto_reject": auto_reject,
            "roadmap": roadmap,                   # STEP 3
            "feedback": feedback,                 # STEP 4
            "interview_questions": interview_questions  # STEP 6
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
