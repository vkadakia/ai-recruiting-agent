import os
from crewai import Agent, LLM


def _llm() -> LLM:
    return LLM(model=os.getenv("MODEL", "openai/gpt-4o-mini"), temperature=0)


def orchestrator_agent() -> Agent:
    return Agent(
        role="Recruiting Orchestrator",
        goal="Coordinate specialist agents and produce a grounded recruiter-facing result.",
        backstory="You are the lead recruiter coordinating specialist AI agents. Never invent candidate qualifications.",
        allow_delegation=False,
        verbose=True,
        llm=_llm(),
    )


def job_analysis_agent() -> Agent:
    return Agent(
        role="Job Analysis Agent",
        goal="Convert a job description into a structured hiring rubric.",
        backstory="You distinguish explicit requirements from preferences and never add unsupported criteria.",
        allow_delegation=False,
        verbose=True,
        llm=_llm(),
    )


def resume_analysis_agent() -> Agent:
    return Agent(
        role="Resume Analysis Agent",
        goal="Extract candidate qualifications and evidence from a resume without guessing.",
        backstory="You normalize resume content into structured facts and preserve uncertainty.",
        allow_delegation=False,
        verbose=True,
        llm=_llm(),
    )


def candidate_evaluation_agent() -> Agent:
    return Agent(
        role="Candidate Evaluation Agent",
        goal="Compare candidate evidence with the hiring rubric and explain fit.",
        backstory="You are evidence-driven, job-related, fair, and explicit about uncertainty.",
        allow_delegation=False,
        verbose=True,
        llm=_llm(),
    )
