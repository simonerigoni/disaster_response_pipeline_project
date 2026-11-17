import pandas as pd
from sqlalchemy import create_engine

from src.config import TABLE_NAME
from src.data_preparation.etl_pipeline import clean_data, load_data, parse_input_arguments, process


def _tiny_messages(path):
    pd.DataFrame(
        {
            "id": [1, 2, 2],
            "message": ["Need water", "Hello", "Hello"],
            "original": ["", "", ""],
            "genre": ["direct", "direct", "direct"],
        }
    ).to_csv(path, index=False)


def _tiny_categories(path):
    pd.DataFrame(
        {
            "id": [1, 2, 2],
            "categories": [
                "related-1;request-1;offer-0",
                "related-1;request-0;offer-0",
                "related-1;request-0;offer-0",
            ],
        }
    ).to_csv(path, index=False)


def test_load_and_clean_data_expands_categories_and_drops_duplicates(tmp_path):
    messages = tmp_path / "messages.csv"
    categories = tmp_path / "categories.csv"
    _tiny_messages(messages)
    _tiny_categories(categories)

    raw = load_data(str(messages), str(categories))
    assert list(raw.columns) == ["id", "message", "original", "genre", "categories"]
    # Duplicate ids in both files produce a many-to-many merge (1 + 2*2 = 5 rows).
    assert len(raw) == 5

    cleaned = clean_data(raw)
    assert "categories" not in cleaned.columns
    assert {"related", "request", "offer"} <= set(cleaned.columns)
    assert cleaned["related"].tolist() == [1, 1]
    assert cleaned["request"].tolist() == [1, 0]
    assert len(cleaned) == 2  # duplicate dropped


def test_process_writes_sqlite_table(tmp_path):
    messages = tmp_path / "messages.csv"
    categories = tmp_path / "categories.csv"
    database = tmp_path / "db.sqlite3"
    _tiny_messages(messages)
    _tiny_categories(categories)

    process(str(messages), str(categories), str(database))
    assert database.is_file()
    engine = create_engine(f"sqlite:///{database}")
    saved = pd.read_sql_table(TABLE_NAME, engine)
    assert len(saved) == 2
    assert "request" in saved.columns


def test_parse_input_arguments_defaults_and_overrides(monkeypatch):
    monkeypatch.setattr("sys.argv", ["etl_pipeline.py"])
    messages, categories, database = parse_input_arguments()
    assert messages.endswith("disaster_messages.csv")
    assert categories.endswith("disaster_categories.csv")
    assert database.endswith("db.sqlite3")

    monkeypatch.setattr(
        "sys.argv",
        [
            "etl_pipeline.py",
            "--messages_filename",
            "m.csv",
            "--categories_filename",
            "c.csv",
            "--database_filename",
            "db.sqlite3",
        ],
    )
    messages, categories, database = parse_input_arguments()
    assert (messages, categories, database) == ("m.csv", "c.csv", "db.sqlite3")
