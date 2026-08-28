from .schemas import CandidateEvaluation


def print_evaluation(result: CandidateEvaluation) -> None:
    width = 68
    print("\n" + "=" * width)
    print("CANDIDATE RESULT".center(width))
    print("=" * width)
    print(f"Candidate:      {result.candidate_name or 'Not provided'}")
    print(f"Recommendation: {result.recommendation}")
    print("\nSUMMARY")
    print(result.summary)

    if result.strengths:
        print("\nSTRENGTHS")
        for item in result.strengths:
            print(f"  • {item}")

    if result.gaps:
        print("\nGAPS")
        for item in result.gaps:
            print(f"  • {item}")

    if result.uncertainties:
        print("\nUNCERTAINTIES")
        for item in result.uncertainties:
            print(f"  • {item}")

    print("\nREQUIREMENT EVIDENCE")
    for item in result.requirement_evidence:
        print(f"  [{item.assessment}] {item.requirement}")
        for evidence in item.evidence or ["No direct resume evidence"]:
            print(f"      - {evidence}")

    print("\nRECRUITER NEXT STEP")
    print(result.recruiter_next_step)
    print("=" * width)
