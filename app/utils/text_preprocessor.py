import re
from typing import Optional

def preprocess_text(text: str) -> str:
    if not text:
        return ""

    # Remove noise
    cleaned_lines = []
    for line in text.splitlines():
        non_alpha_ratio = len(re.findall(r'\W', line)) / (len(line) + 1e-5)
        if non_alpha_ratio < 0.6:
            cleaned_lines.append(line.strip())
    text = "\n".join(cleaned_lines)

    # Normalize spaces
    text = re.sub(r'[ \t]+', ' ', text).strip()

    return text
