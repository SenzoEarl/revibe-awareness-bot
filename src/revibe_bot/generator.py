"""Evidence-constrained post generation helpers. LLM integration belongs behind this interface."""
from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceItem:
    source: str
    url: str
    published_date: str
    attributed_text: str

@dataclass(frozen=True)
class GenerationResult:
    text: str
    evidence_ids: tuple[str, ...]
    insufficient_evidence: bool

def deterministic_pattern_post(category: str, period: str, items: list[EvidenceItem]) -> GenerationResult:
    if len(items) < 3:
        return GenerationResult("INSUFFICIENT_EVIDENCE", (), True)
    sources = ", ".join(item.source for item in items[:3])
    text = (f"Multiple publicly posted customer reports describe {category} issues during {period}. "
            f"These are reported experiences, not a finding of misconduct. Sources: {sources}.")
    return GenerationResult(text, tuple(str(i) for i in range(len(items))), False)
