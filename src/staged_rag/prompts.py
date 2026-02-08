from __future__ import annotations


def staged_rag_system_prompt(question: str) -> str:
    """System prompt that enforces staged retrieval workflow."""
    return (
        "You are a knowledge assistant with access to a staged RAG system.\n\n"
        "RETRIEVAL PROTOCOL:\n"
        "1) SEARCH: call search_summaries with the user's question.\n"
        "2) EVALUATE: read summaries and scores.\n"
        "3) EXPAND: call get_documents for relevant docs only.\n"
        "4) SYNTHESIZE: answer using retrieved content.\n"
        "5) CITE: reference doc_ids for claims.\n\n"
        f"USER QUESTION: {question}"
    )


def evaluate_summaries_prompt(summaries_json: str) -> str:
    """Prompt to decide which summaries to expand."""
    return (
        "Review these search results and decide which documents need expansion.\n"
        "For each document: EXPAND or SKIP with a reason.\n\n"
        f"SUMMARIES:\n{summaries_json}"
    )


def deep_analysis_prompt(question: str, context: str) -> str:
    """Prompt for analysis after context has been retrieved."""
    return (
        "Analyze the following retrieved context to answer the question.\n"
        "Use only the provided context and cite doc_ids.\n\n"
        f"QUESTION: {question}\n\n"
        f"RETRIEVED CONTEXT:\n{context}"
    )
