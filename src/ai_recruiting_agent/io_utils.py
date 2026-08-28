import json
from pathlib import Path
from .schemas import JobRubric


def read_text_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {p}")
    return text


def save_job_rubric(rubric: JobRubric, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rubric.model_dump(), indent=2) + "\n", encoding="utf-8")


def load_job_rubric(path: str) -> JobRubric:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Rubric not found: {p}")
    return JobRubric.model_validate_json(p.read_text(encoding="utf-8"))
