import streamlit as st
import pandas as pd
from ranker import rank_resumes
from pdfreport import generate_pdf_report   # STEP 5D
from emailgenerator import generate_email   # ✅ STEP D3 ADDED


# =====================================================
# STEP 2 — HR DECISION FUNCTION
# =====================================================
def hr_decision(score, cutoff, auto_reject):
    if auto_reject:
        return "REJECT"
    elif score >= cutoff + 10:
        return "HIRE"
    elif score >= cutoff:
        return "HOLD"
    else:
        return "REJECT"


# =====================================================
# STEP 1A — ATS SCORE BAR FUNCTION
# =====================================================
def ats_score_bar(score):
    if score >= 75:
        st.success(f"🟢 ATS Score: {score}% (Strong Match)")
    elif score >= 55:
        st.warning(f"🟡 ATS Score: {score}% (Needs Improvement)")
    else:
        st.error(f"🔴 ATS Score: {score}% (Weak Match)")

    st.progress(min(score / 100, 1.0))


# =====================================================
# STEP 4 — HR REPORT GENERATOR (CSV)
# =====================================================
def generate_hr_report(results, cutoff):
    rows = []

    for r in results:
        decision = hr_decision(r["score"], cutoff, r["auto_reject"])

        rows.append({
            "Candidate Name": r["name"],
            "ATS Score": r["score"],
            "HR Decision": decision,
            "Auto Rejected": "YES" if r["auto_reject"] else "NO",
            "Matched Skills": ", ".join(r["matched_skills"]),
            "Missing Skills": ", ".join(r["missing_skills"]),
            "Rejection Reasons": " | ".join(r["reasons"]),
            "Improvement Estimate (%)": r["improvement_estimate"]
        })

    return pd.DataFrame(rows)


# =====================================================
# UI STYLES
# =====================================================
st.markdown("""
<style>
.block-container {
    max-width: 96% !important;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}
.stApp {
    background: radial-gradient(circle at top,#1e293b 0%,#0f172a 45%,#020617 100%);
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<h1>🤖 AI Resume Screening & Ranking System</h1>
<p>Upload resumes, analyze skills, and get clear hiring decisions</p>
<hr>
""", unsafe_allow_html=True)


# =====================================================
# HR CONTROL
# =====================================================
cutoffscore = st.slider("🎚️ Select cutoff score", 30, 90, 60, 5)
st.divider()


# =====================================================
# INPUT SECTION
# =====================================================
left, right = st.columns(2)

with left:
    resume_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

with right:
    job_text = st.text_area("Paste Job Description", height=220)

st.divider()


# =====================================================
# ANALYZE BUTTON
# =====================================================
if st.button("🚀 Analyze & Rank Candidates", use_container_width=True):

    if resume_files and job_text.strip():
        ranked_results = rank_resumes(resume_files, job_text)

        st.subheader("📊 Candidate Results")

        for idx, result in enumerate(ranked_results, start=1):

            decision = hr_decision(
                result["score"],
                cutoffscore,
                result["auto_reject"]
            )

            with st.container():
                st.markdown(f"""
                ### 🧑 Candidate Rank {idx}
                **File Name:** {result['name']}  
                **Match Score:** {result['score']} %
                """)

                ats_score_bar(result["score"])

                # =============================
                # HR DECISION
                # =============================
                if decision == "HIRE":
                    st.success("🟢 HR DECISION: HIRE (Proceed to Interview)")
                    st.write(result["matched_skills"])

                elif decision == "HOLD":
                    st.warning("🟡 HR DECISION: HOLD")
                    st.write(result["missing_skills"])

                else:
                    st.error("🔴 HR DECISION: REJECTED")
                    st.write(result["missing_skills"])
                    for reason in result["reasons"]:
                        st.write("• " + reason)

                # =============================
                # ROADMAP
                # =============================
                st.markdown("### 🧭 Resume Improvement Roadmap")
                for step in result["roadmap"]:
                    st.write(step)

                # =============================
                # HR FEEDBACK
                # =============================
                st.markdown("**🤖 HR Feedback**")
                st.write(result["feedback"])

                # =====================================================
                # ✅ STEP D3 — EMAIL PREVIEW (HIRE / HOLD / REJECT)
                # =====================================================
                st.markdown("### 📧 HR Email Preview")

                email_subject, email_body = generate_email(
                    candidate_name=result["name"],
                    decision=decision,
                    job_title="Software Engineer"
                )

                st.text_input("Email Subject", email_subject)
                st.text_area("Email Body", email_body, height=220)

                st.download_button(
                    label="⬇️ Download Email (.txt)",
                    data=f"Subject: {email_subject}\n\n{email_body}",
                    file_name=f"{result['name']}_{decision}_email.txt",
                    mime="text/plain"
                )

                # =============================
                # PDF REPORT
                # =============================
                pdf_file = generate_pdf_report(result, decision)

                with open(pdf_file, "rb") as pdf:
                    st.download_button(
                        label="📄 Download ATS PDF Report",
                        data=pdf,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

                st.divider()

        # =====================================================
        # CSV REPORT
        # =====================================================
        st.subheader("📥 Download ATS HR Report")

        report_df = generate_hr_report(ranked_results, cutoffscore)

        st.download_button(
            label="⬇️ Download HR ATS Report (CSV)",
            data=report_df.to_csv(index=False),
            file_name="ATS_HR_Report.csv",
            mime="text/csv"
        )

    else:
        st.warning("⚠️ Please upload resumes and enter a job description")
