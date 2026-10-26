"""
Word Count Tool for LangChain.
Calculates word count, character count, and sentence metrics for supplied text.
"""

import re
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class WordCountInput(BaseModel):
    text: str = Field(description="The text content whose words and statistics need to be counted.")


@tool("word_count", args_schema=WordCountInput)
def count_words(text: str) -> str:
    """
    Counts the number of words, characters (with and without whitespace), and estimated sentences in a given text.
    """
    clean_text = text.strip()
    if not clean_text:
        return "Word Count: 0 words, 0 characters."

    words = clean_text.split()
    word_count = len(words)
    char_count = len(clean_text)
    char_no_spaces = len(re.sub(r"\s+", "", clean_text))
    sentences = [s for s in re.split(r"[.!?]+", clean_text) if s.strip()]
    sentence_count = len(sentences)

    return (
        f"Text Analysis Results:\n"
        f"- Total Words: {word_count}\n"
        f"- Characters (with spaces): {char_count}\n"
        f"- Characters (no spaces): {char_no_spaces}\n"
        f"- Sentence Count: {sentence_count}"
    )
