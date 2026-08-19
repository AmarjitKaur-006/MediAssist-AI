from pathlib import Path
from typing import List

from langchain_core.documents import Document


def load_knowledge_documents(knowledge_dir: str) -> List[Document]:
    """
    Load all Markdown knowledge files and convert them
    into LangChain Document objects.

    Expected structure:
        data/knowledge/
            category/
                test_name.md

    Example:
        data/knowledge/cbc/hemoglobin.md
    """

    knowledge_path = Path(knowledge_dir)

    if not knowledge_path.exists():
        raise FileNotFoundError(
            f"Knowledge directory not found: {knowledge_path}"
        )

    if not knowledge_path.is_dir():
        raise NotADirectoryError(
            f"Expected a directory, got: {knowledge_path}"
        )

    documents: List[Document] = []

    for file_path in sorted(knowledge_path.rglob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        relative_path = file_path.relative_to(knowledge_path)

        parts = relative_path.parts

        category = parts[0] if len(parts) > 1 else "unknown"
        test_name = file_path.stem

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(relative_path).replace("\\", "/"),
                    "category": category,
                    "test_name": test_name,
                },
            )
        )

    return documents