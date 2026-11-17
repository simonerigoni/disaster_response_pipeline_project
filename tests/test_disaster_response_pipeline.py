import pandas as pd
from sqlalchemy import create_engine

import disaster_response_pipeline as pipeline
from src.config import TABLE_NAME


def _write_db(path):
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "message": ["a", "b", "c"],
            "original": ["", "", ""],
            "genre": ["direct", "news", "direct"],
            "related": [1, 1, 1],
            "request": [1, 0, 1],
            "offer": [0, 0, 0],
        }
    )
    engine = create_engine(f"sqlite:///{path}")
    df.to_sql(TABLE_NAME, engine, index=False, if_exists="replace")


def test_category_and_genre_helpers(tmp_path):
    db = tmp_path / "db.sqlite3"
    _write_db(db)
    assert pipeline.get_category_names(str(db)) == ["related", "request", "offer"]
    assert pipeline.get_genre_distribution(str(db)) == {"direct": 2, "news": 1}
    top = pipeline.get_top_n_categories(str(db), n=3)
    # skips the first (highest) category because of [1:n]
    assert "related" not in top
    assert top["request"] == 2


def test_get_predicted_category_names(tmp_path, monkeypatch):
    db = tmp_path / "db.sqlite3"
    _write_db(db)
    monkeypatch.setattr(pipeline, "DATABASE_FILENAME", str(db))
    assert pipeline.get_predicted_category_names([1, 0, 0]) == ["related"]
    assert pipeline.get_predicted_category_names([1, 1, 0]) == ["related", "request"]
    assert pipeline.get_predicted_category_names([0, 0, 0]) == []
