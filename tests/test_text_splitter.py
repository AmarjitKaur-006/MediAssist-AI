from pathlib import Path

from src.rag.document_loader import load_knowledge_documents
from src.rag.text_splitter import split_documents


KNOWLEDGE_DIR = Path("data/knowledge")


def test_text_splitter():
    print("\n========== TEXT SPLITTER TEST ==========")

    documents = load_knowledge_documents(str(KNOWLEDGE_DIR))

    chunks = split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    # We should have more chunks than original documents.
    assert len(chunks) > len(documents)

    # Every chunk must contain actual content.
    assert all(chunk.page_content.strip() for chunk in chunks)

    # Required original metadata must survive splitting.
    for chunk in chunks:
        assert "source" in chunk.metadata
        assert "category" in chunk.metadata
        assert "test_name" in chunk.metadata

    # Check chunk size.
    assert all(
        len(chunk.page_content) <= 800
        for chunk in chunks
    )

    # Avoid extremely small heading-only chunks.
    tiny_chunks = [
        chunk
        for chunk in chunks
        if len(chunk.page_content.strip()) < 100
    ]

    print(f"Tiny chunks (<100 chars): {len(tiny_chunks)}")

    assert len(tiny_chunks) < len(chunks) * 0.10

    print("\nSample chunks:")

    for chunk in chunks[:3]:
        print("\n--- CHUNK ---")
        print("Source:", chunk.metadata["source"])
        print("Category:", chunk.metadata["category"])
        print("Test:", chunk.metadata["test_name"])
        print("Length:", len(chunk.page_content))
        print(chunk.page_content[:500])

    print("\nText splitter test passed! ✓")


if __name__ == "__main__":
    test_text_splitter()