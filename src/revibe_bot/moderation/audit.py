"""Append-only audit event model for moderation and publishing decisions."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    entity_id: str
    actor: str
    decision: str
    reason: str
    evidence_ids: tuple[str, ...] = ()
    timestamp: str = ""
    previous_hash: str = ""

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode()).hexdigest()


def new_event(*, event_type: str, entity_id: str, actor: str, decision: str, reason: str, evidence_ids: tuple[str, ...] = (), previous_hash: str = "") -> AuditEvent:
    return AuditEvent(
        event_type=event_type,
        entity_id=entity_id,
        actor=actor,
        decision=decision,
        reason=reason,
        evidence_ids=evidence_ids,
        timestamp=datetime.now(timezone.utc).isoformat(),
        previous_hash=previous_hash,
    )
