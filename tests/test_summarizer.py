import src.summarizer as summarizer
import pytest

def test_map_summaries_batches_chunks(monkeypatch):
    chunks = [
        {"page": 1, "chunk": 1, "text": "Text 1"},
        {"page": 1, "chunk": 2, "text": "Text 2"},
        {"page": 2, "chunk": 3, "text": "Text 3"},
        {"page": 2, "chunk": 4, "text": "Text 4"},
        {"page": 3, "chunk": 5, "text": "Text 5"},
        {"page": 3, "chunk": 6, "text": "Text 6"},
    ]

    calls = []

    def fake_summarize_text(text):
        calls.append(text)
        return "Mock summary"

    monkeypatch.setattr(
        summarizer,
        "summarize_text",
        fake_summarize_text
    )

    results = summarizer.map_summaries(chunks, batch_size=5)

    assert len(calls) == 2
    assert len(results) == 2
    assert results[0]["summary"] == "Mock summary"
    assert results[1]["summary"] == "Mock summary"


def test_reduce_summaries(monkeypatch):

    def fake_summarize_text(text):
        return "Final combined summary"

    monkeypatch.setattr(
        summarizer,
        "summarize_text",
        fake_summarize_text
    )

    summaries = [
        {"page": 1, "chunk": 1, "summary": "Python basics"},
        {"page": 2, "chunk": 1, "summary": "Python functions"}
    ]

    result = summarizer.reduce_summaries(summaries)

    assert result == "Final combined summary"


def test_hierarchical_reduce_summaries(monkeypatch):

    def fake_reduce_summaries(batch):
        return "Combined: " + ", ".join(
            item["summary"] for item in batch
        )

    monkeypatch.setattr(
        summarizer,
        "reduce_summaries",
        fake_reduce_summaries
    )

    summaries = [
        {"summary": f"Summary {i}"}
        for i in range(12)
    ]

    result = summarizer.hierarchical_reduce_summaries(
        summaries,
        batch_size=5
    )

    assert result.startswith("Combined:")
    assert "Summary 0" in result


def test_summarize_empty_chunks():

    with pytest.raises(ValueError):
        summarizer.summarize_chunks([])

def test_hierarchical_reduce_empty_summaries():

    with pytest.raises(ValueError):
        summarizer.hierarchical_reduce_summaries([])


def test_invalid_batch_size():

    summaries = [
        {"summary": "Python basics"}
    ]

    with pytest.raises(ValueError):
        summarizer.hierarchical_reduce_summaries(
            summaries,
            batch_size=1
        )

def test_summarize_chunks(monkeypatch):

    def fake_map_summaries(chunks):
        return [{"summary": "Mapped summary"}]

    def fake_hierarchical_reduce(summaries, batch_size=5):
        return "Final study notes"

    monkeypatch.setattr(
        summarizer,
        "map_summaries",
        fake_map_summaries
    )

    monkeypatch.setattr(
        summarizer,
        "hierarchical_reduce_summaries",
        fake_hierarchical_reduce
    )

    chunks = [
        {"page": 1, "chunk": 1, "text": "Python basics"}
    ]

    result = summarizer.summarize_chunks(chunks)

    assert result == "Final study notes"