import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from run import app as flask_app

import pytest
from run import app as flask_app  # <-- import app from run.py
from db.connection import get_connection

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_conn():
    conn = get_connection()
    yield conn
    conn.close()
