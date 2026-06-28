from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple


PROJECT_DIR = Path(__file__).resolve().parents[1]
KB_FILE = PROJECT_DIR / "sample_data" / "knowledge_base.md"
OUTPUT_DIR = PROJECT_DIR / "output_samples"
DEMO_FILE = OUTPUT_DIR / "retrieval_demo.md"


Article = Dict[str, str]

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "we",
    "with",
    "you",
    "your",
}

SYNONYMS = {
    "invite": {"invite", "invitation", "teammate", "team", "user"},
    "invoice": {"invoice", "billing", "charged", "seat", "seats", "payment"},
    "refund": {"refund", "cancel", "trial", "charge", "charged"},
    "api": {"api", "sync", "429", "rate", "limit", "salesforce"},
    "password": {"password", "reset", "expired", "login"},
    "sso": {"sso", "identity", "provider", "access", "denied"},
    "dashboard": {"dashboard", "data", "missing", "sync", "integration"},
    "export": {"export", "csv", "report", "analytics"},
}


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    expanded: List[str] = []
    for word in words:
        if word not in STOPWORDS:
            expanded.append(word)
        for values in SYNONYMS.values():
            if word in values:
                expanded.extend(values)
    return expanded


def load_articles() -> List[Article]:
    content = KB_FILE.read_text(encoding="utf-8")
    articles: List[Article] = []
    current_title = ""
    current_lines: List[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_title:
                articles.append({"title": current_title, "body": "\n".join(current_lines).strip()})
            current_title = line.replace("## ", "").strip()
            current_lines = []
        elif current_title:
            current_lines.append(line)

    if current_title:
        articles.append({"title": current_title, "body": "\n".join(current_lines).strip()})

    return articles


def score_article(query: str, article: Article) -> float:
    query_tokens = tokenize(query)
    article_tokens = set(tokenize(article["title"] + " " + article["body"]))
    if not query_tokens or not article_tokens:
        return 0.0

    matches = sum(1 for token in query_tokens if token in article_tokens)
    title_bonus = sum(1 for token in query_tokens if token in tokenize(article["title"])) * 0.4
    return round(min(0.99, (matches + title_bonus) / max(4, len(set(query_tokens)))), 2)


def retrieve(query: str, top_n: int = 1) -> List[Tuple[Article, float]]:
    scored = [(article, score_article(query, article)) for article in load_articles()]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_n]


def demo() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    queries = [
        "teammate did not receive invite email",
        "invoice has extra seats and customer wants correction",
        "Salesforce API sync failing with 429",
        "export weekly activity report as csv",
    ]

    lines = ["# Retrieval Demo", ""]
    for query in queries:
        article, confidence = retrieve(query)[0]
        lines.extend(
            [
                f"## Query: {query}",
                "",
                f"- Matched article: {article['title']}",
                f"- Confidence: {confidence}",
                f"- Excerpt: {article['body'][:220]}",
                "",
            ]
        )

    DEMO_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Retrieval demo written to {DEMO_FILE}")


if __name__ == "__main__":
    demo()

