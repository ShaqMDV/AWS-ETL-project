import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys
 
# Add the src directory to the Python path

sys.path.insert(0, "src")
 
from load_data import connect_to_database, load_json, insert_data
 
class TestLoadData(unittest.TestCase):
 
    @patch("load_data.psycopg2.connect")

    def test_connect_to_database_success(self, mock_connect):

        # Mock successful connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        connection = connect_to_database()
        mock_connect.assert_called_once()
        self.assertEqual(connection, mock_connection)

    @patch("load_data.psycopg2.connect")

    def test_connect_to_database_failure(self, mock_connect):

        # Mock connection failure
        mock_connect.side_effect = Exception("Connection failed")
        connection = connect_to_database()
        mock_connect.assert_called_once()
        self.assertIsNone(connection)
 
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{"key": "value"}')

    def test_load_json_success(self, mock_open):

        # Test loading valid JSON
        file_path = "test.json"
        data = load_json(file_path)
        mock_open.assert_called_once_with(file_path, "r")
        self.assertEqual(data, {"key": "value"})
 
    @patch("builtins.open", side_effect=FileNotFoundError)

    def test_load_json_file_not_found(self, mock_open):

        # Test handling file not found
        file_path = "nonexistent.json"
        data = load_json(file_path)
        mock_open.assert_called_once_with(file_path, "r")
        self.assertIsNone(data)
 
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="invalid json")

    def test_load_json_invalid_json(self, mock_open):

        # Test handling invalid JSON
        file_path = "test.json"
        data = load_json(file_path)
        mock_open.assert_called_once_with(file_path, "r")
        self.assertIsNone(data)
 
    @patch("load_data.psycopg2.connect")

    def test_insert_data_success(self, mock_connect):

        # Mock successful data insertion
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        data = [{"col1": "value1", "col2": "value2"}]
        table_name = "test_table"
        insert_data(mock_connection, table_name, data)
        mock_cursor.execute.assert_called_once_with(

            "INSERT INTO test_table (col1, col2) VALUES (%(col1)s, %(col2)s)", data[0]

        )

        mock_connection.commit.assert_called_once()
 
    @patch("load_data.psycopg2.connect")

    def test_insert_data_failure(self, mock_connect):

        # Mock insertion failure
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Insert failed")
        mock_connect.return_value = mock_connection

        data = [{"col1": "value1", "col2": "value2"}]

        table_name = "test_table"

        insert_data(mock_connection, table_name, data)

        mock_cursor.execute.assert_called_once_with(

            "INSERT INTO test_table (col1, col2) VALUES (%(col1)s, %(col2)s)", data[0]

        )

        mock_connection.rollback.assert_called_once()
 
if __name__ == "__main__":

    unittest.main()