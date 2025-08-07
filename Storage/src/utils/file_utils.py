import os
from typing import Set

def read_text(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return f.read().strip()

def write_text(path: str, content: str) -> None:
    with open(path, 'w') as f:
        f.write(content)

def read_lines(path: str) -> Set[str]:
    if not os.path.exists(path):
        return set()
    with open(path, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def write_lines(path: str, lines: Set[str]) -> None:
    with open(path, 'w') as f:
        for l in sorted(lines):
            f.write(l + "\n")
