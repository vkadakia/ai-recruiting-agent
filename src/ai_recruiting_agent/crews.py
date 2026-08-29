from crewai import Crew, Process, Task

from .agents import candidate_evaluation_agent, job_analysis_agent, orchestrator_agent, resume_analysis_agent
from .schemas import CandidateEvaluation, CandidateProfile, JobRubric


def build_job_rubric(job_description: str) -> JobRubric:
    orchestrator = orchestrator_agent()
    job_analyst = job_analysis_agent()

    framing_task = Task(
        description=f"""Review this job description as the recruiting orchestrator. Prepare a concise brief identifying the role, explicit requirements, preferences, and ambiguities. Do not score candidates.\n\nJOB DESCRIPTION\n{job_description}""",
        expected_output="A concise analysis brief for the Job Analysis Agent.",
        agent=orchestrator,
    )

    rubric_task = Task(
        description=f"""Create a structured hiring rubric from the job description. Only include supported criteria; keep required and preferred criteria separate; do not invent requirements; preserve ambiguity in notes.\n\nJOB DESCRIPTION\n{job_description}""",
        expected_output="A structured JobRubric object.",
        agent=job_analyst,
        context=[framing_task],
        output_pydantic=JobRubric,
    )

    result = Crew(
        agents=[orchestrator, job_analyst],
        tasks=[framing_task, rubric_task],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    if result.pydantic is None:
        raise RuntimeError("CrewAI did not return a structured JobRubric.")
    return result.pydantic


def evaluate_candidate(job_rubric: JobRubric, resume_text: str) -> CandidateEvaluation:
    orchestrator = orchestrator_agent()
    resume_analyst = resume_analysis_agent()
    evaluator = candidate_evaluation_agent()
    rubric_json = job_rubric.model_dump_json(indent=2)

    kickoff_task = Task(
        description=f"""Coordinate evaluation of one candidate. Prepare a short work plan. Require evidence grounding and treat omitted information as UNKNOWN rather than automatically negative.\n\nJOB RUBRIC\n{rubric_json}\n\nRESUME\n{resume_text}""",
        expected_output="A concise evaluation work plan.",
        agent=orchestrator,
    )

    resume_task = Task(
        description=f"""Extract a structured CandidateProfile from this resume. Use only supported facts, do not infer unlisted skills, preserve uncertainties, and do not decide fit yet.\n\nRESUME\n{resume_text}""",
        expected_output="A structured CandidateProfile object.",
        agent=resume_analyst,
        context=[kickoff_task],
        output_pydantic=CandidateProfile,
    )

    evaluation_task = Task(
        description=f"""Compare the candidate profile against this JobRubric. For each meaningful criterion identify evidence and classify it as meets, partially_meets, does_not_meet, or unknown. Missing evidence is usually unknown. Preferred criteria are not hard requirements. Recommend STRONG_MATCH, POTENTIAL_MATCH, or NOT_A_MATCH and explain why. Do not use protected or non-job-related characteristics.\n\nJOB RUBRIC\n{rubric_json}""",
        expected_output="A structured CandidateEvaluation object.",
        agent=evaluator,
        context=[resume_task],
        output_pydantic=CandidateEvaluation,
    )

    final_task = Task(
        description="Review the specialist evaluation as the Recruiting Orchestrator and return the final CandidateEvaluation. Do not invent evidence. Preserve uncertainties and provide a practical recruiter next step.",
        expected_output="The final structured CandidateEvaluation.",
        agent=orchestrator,
        context=[evaluation_task],
        output_pydantic=CandidateEvaluation,
    )

    result = Crew(
        agents=[orchestrator, resume_analyst, evaluator],
        tasks=[kickoff_task, resume_task, evaluation_task, final_task],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    if result.pydantic is None:
        raise RuntimeError("CrewAI did not return a structured CandidateEvaluation.")
    return result.pydantic
