"""Tools for research agent."""

from tools.web_search import web_search
from tools.web_fetch import web_fetch
from tools.summarizer import summarize_content
from tools.pdf_generator import generate_pdf_report

ALL_TOOLS = [
    web_search,
    web_fetch,
    summarize_content,
    generate_pdf_report,
]
