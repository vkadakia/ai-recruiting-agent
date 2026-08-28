import argparse
from dotenv import load_dotenv

from .crews import build_job_rubric, evaluate_candidate
from .io_utils import load_job_rubric, read_text_file, save_job_rubric
from .presentation import print_evaluation


def setup_job(job_description_path: str, rubric_output_path: str) -> None:
    print("\nAI RECRUITING SYSTEM — JOB SETUP")
    print("→ Loading job description")
    job_description = read_text_file(job_description_path)
    print("→ Orchestrator + Job Analysis Agent")
    rubric = build_job_rubric(job_description)
    save_job_rubric(rubric, rubric_output_path)
    print(f"\n✓ Rubric saved to {rubric_output_path}")
    print(f"✓ Role: {rubric.role_title}")
    print(f"✓ Required criteria: {len(rubric.required_requirements)}")
    print(f"✓ Preferred criteria: {len(rubric.preferred_requirements)}")


def evaluate(rubric_path: str, resume_path: str) -> None:
    print("\nAI RECRUITING SYSTEM — CANDIDATE EVALUATION")
    print("→ Loading existing job rubric")
    rubric = load_job_rubric(rubric_path)
    print("→ Loading resume")
    resume_text = read_text_file(resume_path)
    print("→ Orchestrator + Resume Analysis Agent + Candidate Evaluation Agent")
    result = evaluate_candidate(rubric, resume_text)
    print_evaluation(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple CrewAI recruiting demo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup = subparsers.add_parser("setup-job", help="Analyze a job description once and save a reusable rubric.")
    setup.add_argument("job_description", help="Path to job_description.txt")
    setup.add_argument("rubric_output", help="Path for generated job_rubric.json")

    candidate = subparsers.add_parser("evaluate", help="Evaluate one resume against an existing job rubric.")
    candidate.add_argument("job_rubric", help="Path to job_rubric.json")
    candidate.add_argument("resume", help="Path to resume.txt")
    return parser


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()
    if args.command == "setup-job":
        setup_job(args.job_description, args.rubric_output)
    elif args.command == "evaluate":
        evaluate(args.job_rubric, args.resume)


if __name__ == "__main__":
    main()
