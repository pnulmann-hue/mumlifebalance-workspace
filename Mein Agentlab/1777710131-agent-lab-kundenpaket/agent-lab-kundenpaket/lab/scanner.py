"""
scanner.py — Liest alle Agent-Configs aus dem Dateisystem.

Scannt Python-Dateien nach SYSTEM_PROMPT, Keywords, Model-Config
und erstellt einen vollstaendigen Snapshot aller Agents.
"""
from __future__ import annotations

import ast
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class AgentSnapshot:
    name: str
    file_path: str
    system_prompt: str
    keywords: list[str] = field(default_factory=list)
    model: str = ""
    max_turns: int = 0
    max_tokens: int = 0
    tools: list[str] = field(default_factory=list)
    last_modified: float = 0.0
    raw_content: str = ""

    def summary(self) -> str:
        prompt_preview = self.system_prompt[:150].replace("\n", " ")
        return (
            f"{self.name}\n"
            f"  Datei: {self.file_path}\n"
            f"  Model: {self.model or '(nicht gesetzt)'}\n"
            f"  Max Turns: {self.max_turns}, Max Tokens: {self.max_tokens}\n"
            f"  Keywords: {len(self.keywords)}\n"
            f"  Tools: {', '.join(self.tools) or '(keine)'}\n"
            f"  Prompt: {prompt_preview}..."
        )


# Pfade zu deinen Agents.
# - Relative Pfade sind relativ zu vault_root ("Mein Agentlab/").
# - "~" wird zu deinem Benutzerordner expandiert (C:\Users\pnulm).
# - Absolute Pfade werden direkt genutzt.
# Unterstuetzte Prompt-Formate: Python (SYSTEM_PROMPT/system_prompt = """...""")
# und TypeScript/JS (SYSTEM_PROMPT/systemPrompt = `...`).
AGENT_FILES = [
    # Python-Bot in diesem Workspace
    {"name": "garten_bot", "path": "../scripts/garten-telegram-bot/config.py"},
    # TypeScript-Bots in eigenen Repos (~ = C:\Users\pnulm)
    {"name": "doterra_bot", "path": "~/doterra-bot/lib/system-prompt.ts"},
    {"name": "doterra_newsletter", "path": "~/doterra-bot/lib/newsletter-generator.ts"},
    {"name": "koch_bot", "path": "~/koch-bot/lib/system-prompt.ts"},
    {"name": "business_bot", "path": "~/business-bot/lib/system-prompt.ts"},
]


def resolve_agent_path(path_str: str, vault_root: Path) -> Path:
    """Loest einen Agent-Pfad auf:
    ~ wird expandiert, absolute Pfade bleiben, relative haengen an vault_root."""
    expanded = Path(os.path.expanduser(path_str))
    if expanded.is_absolute():
        return expanded
    return vault_root / path_str


class AgentScanner:
    """Scans all known agent files and extracts their configuration."""

    def __init__(self, vault_root: str = None):
        if vault_root is None:
            vault_root = os.path.join(os.path.dirname(__file__), "..", "..", "..")
        self._vault_root = Path(vault_root).resolve()

    def scan_all(self) -> list[AgentSnapshot]:
        snapshots = []
        for agent_def in AGENT_FILES:
            path = resolve_agent_path(agent_def["path"], self._vault_root)
            if not path.exists():
                continue
            snapshot = self._scan_file(agent_def["name"], str(path))
            if snapshot:
                snapshots.append(snapshot)
        return snapshots

    def scan_one(self, name: str) -> Optional[AgentSnapshot]:
        for agent_def in AGENT_FILES:
            if agent_def["name"] == name:
                path = resolve_agent_path(agent_def["path"], self._vault_root)
                if path.exists():
                    return self._scan_file(name, str(path))
        return None

    def _scan_file(self, name: str, file_path: str) -> Optional[AgentSnapshot]:
        try:
            content = Path(file_path).read_text(encoding="utf-8")
        except OSError:
            return None

        snapshot = AgentSnapshot(
            name=name,
            file_path=file_path,
            system_prompt="",
            last_modified=os.path.getmtime(file_path),
            raw_content=content,
        )

        # Extract SYSTEM_PROMPT — Python ("""/'''/") und TypeScript/JS (Backticks `...`).
        # Variablennamen: SYSTEM_PROMPT, system_prompt, systemPrompt.
        prompt_patterns = [
            r'(?:SYSTEM_PROMPT|system_prompt|systemPrompt)\s*=\s*"""(.*?)"""',
            r"(?:SYSTEM_PROMPT|system_prompt|systemPrompt)\s*=\s*'''(.*?)'''",
            r'(?:SYSTEM_PROMPT|system_prompt|systemPrompt)\s*=\s*`(.*?)`',
            r'(?:SYSTEM_PROMPT|system_prompt|systemPrompt)\s*=\s*"(.*?)"',
        ]
        for pattern in prompt_patterns:
            prompt_match = re.search(pattern, content, re.DOTALL)
            if prompt_match and prompt_match.group(1).strip():
                snapshot.system_prompt = prompt_match.group(1)
                break

        # Extract keywords list
        kw_match = re.search(r'keywords\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if kw_match:
            raw = kw_match.group(1)
            snapshot.keywords = re.findall(r'"([^"]+)"', raw)

        # Extract model
        model_match = re.search(r'model\s*=\s*"([^"]+)"', content)
        if model_match:
            snapshot.model = model_match.group(1)
        elif "CLAUDE_MODEL" in content:
            model_var = re.search(r'CLAUDE_MODEL\s*=\s*"([^"]+)"', content)
            if model_var:
                snapshot.model = model_var.group(1)

        # Extract max_turns
        mt_match = re.search(r'max_turns\s*=\s*(\d+)', content)
        if mt_match:
            snapshot.max_turns = int(mt_match.group(1))

        # Extract max_tokens
        mtk_match = re.search(r'max_tokens\s*=\s*(\d+)', content)
        if mtk_match:
            snapshot.max_tokens = int(mtk_match.group(1))

        # Extract tool class names
        tool_matches = re.findall(r'(\w+Tool)\(\)', content)
        snapshot.tools = list(set(tool_matches))

        return snapshot
