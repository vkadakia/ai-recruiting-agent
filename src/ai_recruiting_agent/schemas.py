from typing import Literal
from pydantic import BaseModel, Field


class Requirement(BaseModel):
    name: str
    description: str
    importance: Literal["required", "preferred"]
    evidence_expected: list[str] = Field(default_factory=list)


class JobRubric(BaseModel):
    role_title: str
    role_summary: str
    required_requirements: list[Requirement]
    preferred_requirements: list[Requirement]
    responsibilities: list[str] = Field(default_factory=list)
    disqualifiers: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class CandidateEvidence(BaseModel):
    requirement: str
    evidence: list[str] = Field(default_factory=list)
    assessment: Literal["meets", "partially_meets", "does_not_meet", "unknown"]


class CandidateProfile(BaseModel):
    candidate_name: str | None = None
    summary: str
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    notable_achievements: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)


class CandidateEvaluation(BaseModel):
    candidate_name: str | None = None
    recommendation: Literal["STRONG_MATCH", "POTENTIAL_MATCH", "NOT_A_MATCH"]
    summary: str
    requirement_evidence: list[CandidateEvidence]
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    recruiter_next_step: str
