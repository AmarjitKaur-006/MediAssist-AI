from pathlib import Path

from langchain_core.documents import Document

from src.rag.document_loader import load_knowledge_documents


KNOWLEDGE_DIR = Path("data/knowledge")


def test_document_loader():
    print("\n========== DOCUMENT LOADER TEST ==========")

    documents = load_knowledge_documents(str(KNOWLEDGE_DIR))

    print(f"Total documents loaded: {len(documents)}")

    # 1. Verify total document count
    assert len(documents) == 68, (
        f"Expected 68 documents, but loaded {len(documents)}"
    )

    # 2. Verify every item is a LangChain Document
    assert all(isinstance(doc, Document) for doc in documents)

    # 3. Verify every document has content
    assert all(doc.page_content.strip() for doc in documents)

    # 4. Verify required metadata exists
    for doc in documents:
        assert "source" in doc.metadata
        assert "category" in doc.metadata
        assert "test_name" in doc.metadata

        assert doc.metadata["source"]
        assert doc.metadata["category"]
        assert doc.metadata["test_name"]

    # 5. Verify expected categories exist
    categories = {
        doc.metadata["category"]
        for doc in documents
    }

    expected_categories = {
        "cbc",
        "electrolytes",
        "glucose",
        "inflammation",
        "iron",
        "kidney",
        "lipid",
        "liver",
        "thyroid",
        "urinalysis",
        "vitamins",
    }

    assert categories == expected_categories

    # 6. Verify source paths use forward slashes
    assert all(
        "\\" not in doc.metadata["source"]
        for doc in documents
    )

    # 7. Print a few examples
    print("\nSample documents:")

    for doc in documents[:3]:
        print(
            f"- {doc.metadata['source']} "
            f"| category={doc.metadata['category']} "
            f"| test={doc.metadata['test_name']}"
        )

    print("\nDocument loader test passed! ✓")


if __name__ == "__main__":
    test_document_loader()