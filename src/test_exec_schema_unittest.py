import unittest
from unittest.mock import mock_open, patch, MagicMock
import psycopg2
from execute_schema import load_sql_script, execute_sql_script

class TestExecute_Schema(unittest.TestCase):

    #Test sql script file does not exist
    @patch("builtins.open", side_effect=Exception("File not found"))    
    def test_load_sql_script_File_notexist(self, mock_file):
        file_path = "None.sql"
        result = load_sql_script(file_path)
        self.assertIsNone(result)

    #Test empty file
    @patch("builtins.open", new_callable=mock_open)    
    def test_load_sql_script_Failuer(self, mock_file):
            result = load_sql_script("empty.sql")
            self.assertEqual(result, "")
            mock_file.assert_called_once_with("empty.sql", 'r')

    @patch("psycopg2.connect")
    def test_execute_sql_script_success(self, mock_connect):
        """Test executing a SQL script successfully."""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Create a mock cursor that will be returned when connection.cursor() is called
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        script = "CREATE TABLE test (id INT PRIMARY KEY);"
        execute_sql_script(mock_connection, script)
        # Verify that cursor.execute was called with the correct script
        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()

        
    @patch("psycopg2.connect")
    def test_rollback_due_to_sql_script_error(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        # Set up the cursor to behave as a context manager
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        # Configure the mock cursor to raise an exception when execute is called
        mock_cursor.execute.side_effect = psycopg2.Error("SQL script error")
        # Define a sample SQL script that will trigger an error
        sql_script = "create;"
        # Call the function and verify it handles the error properly
        execute_sql_script(mock_connection, sql_script)
        # Assert that the cursor's execute method was called with the SQL script
        mock_cursor.execute.assert_called_once_with(sql_script)
        # Assert that rollback was called once due to the error
        mock_connection.rollback.assert_called_once()

        
if __name__ == "__main__":
        unittest.main()