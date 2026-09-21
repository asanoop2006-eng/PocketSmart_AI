import os
import re
import html

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def format_ai_response(text):
    """
    Converts Gemini's Markdown response
    into simple HTML formatting.
    """

    # Escape unsafe HTML characters
    text = html.escape(text)

    # Convert headings into bold headings
    text = re.sub(
        r"^#{1,6}\s*(.+)$",
        r"<h4>\1</h4>",
        text,
        flags=re.MULTILINE
    )

    # Convert bold Markdown into HTML bold
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        text
    )

    # Convert bullet points
    text = re.sub(
        r"^\s*[-•]\s*(.+)$",
        r"• \1",
        text,
        flags=re.MULTILINE
    )

    # Convert line breaks
    text = text.replace("\n", "<br>")

    return text


def generate_ai_recommendation(prompt):

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        text = response.text or "No AI suggestions available."

        formatted_text = format_ai_response(text)

        return formatted_text

    except Exception:
        return (
            "Gemini AI is temporarily unavailable. "
            "Please check the budget recommendations shown below."
        )