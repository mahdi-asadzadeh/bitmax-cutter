from bitmax_cutter.main import app


def test_app():
    assert app.version is not None
