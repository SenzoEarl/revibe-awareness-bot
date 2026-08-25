"""Provider-neutral AI pipeline boundary.

The provider implementation is deliberately injected. This module never gives
an LLM permission to create evidence; it only validates model output against
application schemas and supplied source records.
"""
from __future__ import annotations

from typing import Protocol, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class StructuredModel(Protocol):
    def generate(self, *, system_prompt: str, input_data: dict, output_type: type[T]) -> T:
        ...


class EvidenceBoundaryError(ValueError):
    pass


def require_source_evidence(input_data: dict) -> None:
    evidence = input_data.get("evidence")
    if not evidence:
        raise EvidenceBoundaryError("model invocation requires supplied evidence")


def run_structured(
    model: StructuredModel,
    *,
    system_prompt: str,
    input_data: dict,
    output_type: type[T],
) -> T:
    require_source_evidence(input_data)
    return model.generate(system_prompt=system_prompt, input_data=input_data, output_type=output_type)
