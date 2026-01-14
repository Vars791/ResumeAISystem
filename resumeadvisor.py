def generateResumeAdvice(missingSkills, reasons, improvementEstimate):
    advice = []

    if missingSkills:
        advice.append(
            "Add or highlight these skills in your resume: "
            + ", ".join(missingSkills)
        )
        advice.append(
            "Work on small projects or certifications related to the missing skills."
        )

    for reason in reasons:
        if "skill match" in reason.lower():
            advice.append(
                "Move the technical skills section to the top and clearly mention experience."
            )

        if "relevance" in reason.lower() or "responsibilities" in reason.lower():
            advice.append(
                "Rewrite resume bullet points using keywords from the job description."
            )

    advice.append(
        f"Improving these areas can increase your ATS score by approximately "
        f"{improvementEstimate}%."
    )

    return advice
