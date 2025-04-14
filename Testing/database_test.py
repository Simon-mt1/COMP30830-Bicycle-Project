import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock
from database import init_db

# Testing/database_test.py

import pytest
from unittest.mock import patch, MagicMock
from database import init_db

class TestDatabaseService:

    @patch('database.Base.metadata.create_all')
    @patch('database.engine')
    @patch('database.db_session')
    def test_init_db_success(self, mock_db_session, mock_engine, mock_create_all):
        # Arrange
        mock_db_session.return_value = True
        mock_create_all.return_value = None

        # Act
        init_db()

        # Assert
        mock_create_all.assert_called_once()

    @patch('database.Base.metadata.create_all')
    @patch('database.engine')
    @patch('database.db_session')
    def test_init_db_error(self, mock_db_session, mock_engine, mock_create_all):
        # Arrange
        mock_create_all.side_effect = Exception("Connection Error")

        # Act and Assert
        with pytest.raises(Exception, match="Connection Error"):
            init_db()

    @patch('database.Base.metadata.create_all')
    @patch('database.engine')
    @patch('database.db_session')
    def test_init_db_with_invalid_config(self, mock_db_session, mock_engine, mock_create_all):
        # Simulate environment variables not set
        with patch('database.os.getenv', return_value=None):
            # Act and Assert
            with pytest.raises(Exception):
                init_db()

