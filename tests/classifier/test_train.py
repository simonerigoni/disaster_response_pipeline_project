import pandas as pd
from sqlalchemy import create_engine

from src.classifier.train import (
    get_df_from_database,
    load_data,
    my_tokenizer,
    parse_input_arguments,
)
from src.config import TABLE_NAME


def test_my_tokenizer_replaces_urls_and_lowercases(monkeypatch):
    # Avoid requiring NLTK corpora in CI; cover URL substitution + lemma/lower path.
    monkeypatch.setattr(
        "src.classifier.train.word_tokenize",
        lambda text: text.replace("!", "").split(),
    )

    class FakeLemmatizer:
        def lemmatize(self, tok):
            return tok

    monkeypatch.setattr("src.classifier.train.WordNetLemmatizer", FakeLemmatizer)
    tokens = my_tokenizer("Please visit https://example.com/help NOW!")
    assert "urlplaceholder" in tokens
    assert "https://example.com/help" not in tokens
    assert "please" in tokens
    assert "now" in tokens
    assert all(token == token.lower() for token in tokens)


def test_load_data_splits_message_and_category_columns(tmp_path):
    engine_path = tmp_path / "db.sqlite3"
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "message": ["a", "b"],
            "original": ["", ""],
            "genre": ["direct", "news"],
            "related": [1, 0],
            "request": [1, 0],
        }
    )
    engine = create_engine(f"sqlite:///{engine_path}")
    df.to_sql(TABLE_NAME, engine, index=False, if_exists="replace")

    loaded = get_df_from_database(str(engine_path))
    pd.testing.assert_frame_equal(loaded, df)

    X, Y, category_names = load_data(str(engine_path))
    assert list(X) == ["a", "b"]
    assert list(Y.columns) == ["related", "request"]
    assert category_names == ["related", "request"]


def test_parse_input_arguments_defaults(monkeypatch):
    monkeypatch.setattr("sys.argv", ["train.py"])
    database, model, grid = parse_input_arguments()
    assert database.endswith("db.sqlite3")
    assert model.endswith(".pkl") or "model" in model or isinstance(model, str)
    assert grid is False
