from __future__ import annotations

import datetime
import enum
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, Field, ValidationError


class AgentPhase(str, enum.Enum):
    INITIALIZING = "initializing"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="agent")
    phase: AgentPhase = Field(default=AgentPhase.INITIALIZING)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    context: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    results: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    progress: float = Field(default=0.0, ge=0.0, le=1.0)
    completed: bool = Field(default=False)

    class Config:
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime.datetime: lambda value: value.isoformat(),
        }

    def touch(self) -> None:
        self.updated_at = datetime.datetime.utcnow()

    def update_phase(self, phase: AgentPhase) -> AgentState:
        self.phase = phase
        self.touch()
        return self

    def add_message(
        self,
        role: str,
        content: Any,
        timestamp: Optional[datetime.datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AgentState:
        message = {
            "role": role,
            "content": content,
            "timestamp": (timestamp or datetime.datetime.utcnow()).isoformat(),
        }
        if metadata:
            message["metadata"] = metadata
        self.messages.append(message)
        self.touch()
        return self

    def add_result(self, name: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> AgentState:
        result = {"name": name, "value": value, "metadata": metadata or {}}
        self.results.append(result)
        self.touch()
        return self

    def record_error(self, error: str) -> AgentState:
        self.errors.append(error)
        self.phase = AgentPhase.FAILED
        self.touch()
        return self

    def set_progress(self, progress: float) -> AgentState:
        self.progress = max(0.0, min(1.0, progress))
        self.touch()
        return self

    def mark_complete(self) -> AgentState:
        self.completed = True
        self.phase = AgentPhase.COMPLETED
        self.set_progress(1.0)
        self.touch()
        return self

    def update_context(self, values: Dict[str, Any]) -> AgentState:
        self.context.update(values)
        self.touch()
        return self

    def update_memory(self, values: Dict[str, Any]) -> AgentState:
        self.memory.update(values)
        self.touch()
        return self

    def set_metadata(self, values: Dict[str, Any]) -> AgentState:
        self.metadata.update(values)
        self.touch()
        return self

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls: Type[AgentState], raw_json: str) -> AgentState:
        return cls.model_validate_json(raw_json)

    @classmethod
    def from_dict(cls: Type[AgentState], payload: Dict[str, Any]) -> AgentState:
        return cls.model_validate(payload)


class AgentStateStore:
    def __init__(self, storage_dir: str | Path):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, state_id: str) -> Path:
        return self.storage_dir / f"{state_id}.json"

    def save(self, state: AgentState) -> Path:
        file_path = self._path_for(state.id)
        file_path.write_text(state.to_json(indent=2), encoding="utf-8")
        return file_path

    def load(self, state_id: str) -> AgentState:
        file_path = self._path_for(state_id)
        if not file_path.exists():
            raise FileNotFoundError(f"State file not found: {file_path}")
        return AgentState.from_json(file_path.read_text(encoding="utf-8"))

    def list_states(self) -> List[str]:
        return [path.stem for path in self.storage_dir.glob("*.json")]

    def delete(self, state_id: str) -> bool:
        file_path = self._path_for(state_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False


def validate_state(raw: Any) -> AgentState:
    if isinstance(raw, AgentState):
        return raw
    if isinstance(raw, str):
        return AgentState.from_json(raw)
    if isinstance(raw, dict):
        return AgentState.from_dict(raw)
    raise ValidationError([{"type": "type_error", "loc": (), "msg": "Unsupported state payload"}], AgentState)


__all__ = ["AgentPhase", "AgentState", "AgentStateStore", "validate_state"]
