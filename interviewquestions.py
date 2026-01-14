def generateInterviewQuestions(matched_skills, missing_skills):
    questions = []

    # Basic intro
    questions.append("Tell us about yourself and your recent projects.")
    questions.append("Explain a challenging problem you solved recently.")

    # Questions from matched skills
    for skill in matched_skills[:3]:
        questions.append(
            f"Explain your experience with {skill} and how you used it in a project."
        )

    # Questions from missing skills
    for skill in missing_skills[:2]:
        questions.append(
            f"You have limited exposure to {skill}. How would you learn it quickly?"
        )

    # Behavioral question
    questions.append(
        "Describe a situation where you had to learn something new under a tight deadline."
    )

    return questions
