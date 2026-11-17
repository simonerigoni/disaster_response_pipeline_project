from src import config


def test_config_paths():
    assert config.DATA_FOLDER == "data/"
    assert config.CATEGORIES_FILENAME.endswith("disaster_categories.csv")
    assert config.MESSAGES_FILENAME.endswith("disaster_messages.csv")
    assert config.DATABASE_FILENAME.endswith("db.sqlite3")
    assert config.TABLE_NAME
