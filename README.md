# AI Recruiting Agent

A deliberately small CrewAI demo that analyzes a job once, saves a reusable rubric, and evaluates resumes against that rubric.

## Agents

1. Recruiting Orchestrator
2. Job Analysis Agent
3. Resume Analysis Agent
4. Candidate Evaluation Agent

For classroom reliability, CrewAI runs the tasks sequentially. The Orchestrator frames/finalizes the work while specialist agents perform the domain analysis.

## Setup

Requires Python 3.10–3.13.

```bash
cd /Users/vkadakia/git/ai-recruiting-agent
uv sync
cp .env.example .env
```

Add your `OPENAI_API_KEY` to `.env`.

## Analyze a job once

```bash
uv run recruit setup-job \
  data/jobs/job_description.txt \
  data/jobs/job_rubric.json
```

This generates `job_rubric.json`, which represents the job and can be reused for any number of candidates.

## Evaluate a candidate

```bash
uv run recruit evaluate \
  data/jobs/job_rubric.json \
  data/resumes/resume.txt
```

To evaluate Candidate 2, pass another resume while keeping the same rubric:

```bash
uv run recruit evaluate \
  data/jobs/job_rubric.json \
  data/resumes/resume2.txt
```

## Important

This is a teaching/demo system, not a production hiring product. It should not be used as the sole basis for employment decisions. Human review remains required.
