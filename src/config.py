# Config
#
# python -m src.config


DATA_FOLDER = 'data/'
IMAGES_FOLDER = 'images/'
CATEGORIES_FILENAME = DATA_FOLDER + 'disaster_categories.csv'
MESSAGES_FILENAME = DATA_FOLDER + 'disaster_messages.csv'
DATABASE_FILENAME = DATA_FOLDER + 'db.sqlite3'
TABLE_NAME = 'disaster_message'
MODEL_PICKLE_FILENAME = DATA_FOLDER + 'trained_classifier.pkl'
DEFAULT_TEST_MESSAGE = 'Storm at sacred heart of Jesus'


if __name__ == "__main__":
    print("Config")
    print(f"{DATA_FOLDER = }")
    print(f"{IMAGES_FOLDER = }")
    print(f"{CATEGORIES_FILENAME = }")
    print(f"{MESSAGES_FILENAME = }")
    print(f"{DATABASE_FILENAME = }")
    print(f"{TABLE_NAME = }")
    print(f"{MODEL_PICKLE_FILENAME = }")
    print(f"{DEFAULT_TEST_MESSAGE = }")
else:
    pass
