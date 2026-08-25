import pytest
from pydantic import BaseModel

from revibe_bot.ai.pipeline import EvidenceBoundaryError, run_structured


class Output(BaseModel):
    value: str


class FakeModel:
    def generate(self, *, system_prompt, input_data, output_type):
        return output_type(value="ok")


def test_ai_requires_evidence():
    with pytest.raises(EvidenceBoundaryError):
        run_structured(FakeModel(), system_prompt="x", input_data={}, output_type=Output)


def test_ai_output_is_schema_validated():
    result = run_structured(
        FakeModel(), system_prompt="x", input_data={"evidence": [{"id": "e1"}]}, output_type=Output
    )
    assert result.value == "ok"
