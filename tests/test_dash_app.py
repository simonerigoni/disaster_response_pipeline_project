"""dash_app.py builds a Dash app at import/_create_app time; cover the factory."""

import dash_app


def test_create_app_is_importable():
    assert callable(dash_app._create_app)
