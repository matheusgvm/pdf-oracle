import re

def preprocess_text(text: str) -> str:
    """
    Preprocess input text by removing noisy lines and normalizing spaces.

    Noise removal criteria:
    - Remove lines where more than 60% of characters are non-alphanumeric.

    Args:
        text (str): Raw text input.

    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""

    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue  # skip empty lines

        non_alpha_chars = re.findall(r'\W', line)
        non_alpha_ratio = len(non_alpha_chars) / max(len(line), 1)

        if non_alpha_ratio < 0.6:
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text).strip()

    return cleaned_text
