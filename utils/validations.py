from __future__ import annotations

import tiktoken

MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024
MAX_TOKENS = 10_000


def get_token_count(text: str, model: str | None = None) -> int:
    """Estimate token count using tiktoken."""
    if not text:
        return 0

    try:
        encoding = tiktoken.encoding_for_model(model or "gpt-4o")
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def validate_text_limits(
    text: str,
    label: str,
    *,
    model: str | None = None,
    max_tokens: int = MAX_TOKENS,
) -> list[str]:
    """Validate the token limit for a text field."""
    errors: list[str] = []
    token_count = get_token_count(text, model=model)

    if token_count > max_tokens:
        errors.append(
            f"{label} exceeds the {max_tokens:,} token limit "
            f"({token_count:,} tokens detected)."
        )

    return errors


def validate_file_size(size_bytes: int | None, label: str, *, max_bytes: int = MAX_FILE_SIZE_BYTES) -> list[str]:
    """Validate the uploaded file size limit."""
    errors: list[str] = []
    if size_bytes is not None and size_bytes > max_bytes:
        errors.append(
            f"{label} exceeds the 1 MB file limit "
            f"({size_bytes:,} bytes detected)."
        )
    return errors
