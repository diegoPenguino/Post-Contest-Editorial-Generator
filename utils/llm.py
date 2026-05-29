from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from langchain_google_genai import ChatGoogleGenerativeAI

from utils.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE

logger = logging.getLogger(__name__)


def create_llm(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    api_key: Optional[str] = None,
) -> ChatGoogleGenerativeAI:
    """Create the Gemini chat model used across the editorial workflow."""
    kwargs = {
        "model": model or DEFAULT_MODEL,
        "temperature": DEFAULT_TEMPERATURE if temperature is None else temperature,
    }
    if api_key:
        kwargs["google_api_key"] = api_key

    logger.debug(
        "Creating Gemini LLM: model=%s temperature=%s api_key_provided=%s",
        kwargs["model"],
        kwargs["temperature"],
        bool(api_key),
    )

    return ChatGoogleGenerativeAI(**kwargs)


def response_content_to_text(content: Any) -> str:
    """Normalize Gemini/LangChain content to a plain text string."""
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if text:
                    parts.append(str(text))
            elif hasattr(part, "text"):
                text = getattr(part, "text")
                if text:
                    parts.append(str(text))
            else:
                parts.append(str(part))
        return "".join(parts)

    if hasattr(content, "text"):
        return str(getattr(content, "text"))

    return str(content)


def log_llm_response(node_name: str, response: Any) -> str:
    """Log useful response diagnostics and return normalized text."""
    content = getattr(response, "content", response)
    text = response_content_to_text(content)

    logger.info(
        "%s response received: response_type=%s content_type=%s text_len=%d",
        node_name,
        type(response).__name__,
        type(content).__name__,
        len(text),
    )
    logger.debug("%s response preview: %s", node_name, text[:500])

    return text


def report_progress(state: dict[str, Any], phase: str) -> None:
    """Send a progress update to the UI if a callback is configured."""
    callback = state.get("progress_callback")
    if callable(callback):
        callback(phase)
