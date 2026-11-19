from src.pdf_processing import split_text_into_chunks


def test_chunking_preserves_page_and_overlap():
    result = split_text_into_chunks([{"page": 2, "text": "abcdefghij"}], chunk_size=6, overlap=2)
    assert [chunk["text"] for chunk in result] == ["abcdef", "efghij"]
    assert all(chunk["page"] == 2 for chunk in result)


def test_empty_page():
    assert split_text_into_chunks([]) == []
