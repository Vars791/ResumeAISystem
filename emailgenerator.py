def generate_email(candidate_name, decision, job_title="the position"):
    if decision == "HIRE":
        subject = f"Interview Invitation – {job_title}"
        body = f"""
Dear {candidate_name},

Congratulations!

We reviewed your profile and are pleased to inform you that you have been
shortlisted for the next round of interviews for {job_title}.

Our HR team will contact you shortly with interview details.

Best regards,
HR Team
"""

    elif decision == "HOLD":
        subject = f"Application Update – {job_title}"
        body = f"""
Dear {candidate_name},

Thank you for applying for {job_title}.

Your profile shows good potential. At this time, we are keeping your resume
in our talent pool for future opportunities.

We appreciate your interest and encourage you to continue improving your skills.

Best regards,
HR Team
"""

    else:
        subject = f"Application Status – {job_title}"
        body = f"""
Dear {candidate_name},

Thank you for taking the time to apply for {job_title}.

After careful review, we will not be moving forward with your application
at this stage.

We encourage you to continue developing your skills and apply again in the future.

Best wishes,
HR Team
"""

    return subject.strip(), body.strip()
