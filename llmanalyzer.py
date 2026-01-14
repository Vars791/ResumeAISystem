def llmanalysis(score, matchedskills, missingskills):
    if score >= 65:
        return (
            "SELECTED\n\n"
            "Reason:\n"
            "Candidate matches most required skills. "
            "Matched skills: " + ", ".join(matchedskills)
        )
    else:
        return (
            "REJECTED\n\n"
            "Reason:\n"
            "Candidate is missing key skills. "
            "Missing skills: " + ", ".join(missingskills)
        )
