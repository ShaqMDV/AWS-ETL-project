import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from unittest.mock import patch, mock_open
import json
from extract_data import read_csv, parse_items, prepare_data, validate_data, save_data_to_json

def test_read_csv():
    # Mock CSV content
    csv_content = """timestamp,location,customer_name,items,total_cost,payment_method,credit_card
    2024-04-21 09:00:00,Edinburgh,John Doe,Regular Coffee - - 2.5,10.00,Cash,1234-5678-9012-3456"""
    with patch("builtins.open", mock_open(read_data=csv_content)):
        data = read_csv("dummy.csv")
    
    assert len(data) == 2  # Header + 1 row
    assert data[1]["timestamp"] == "2024-04-21 09:00:00"  # Check data content

# def test_parse_items_valid():
#     items_column = "Regular Coffee - - 2.5, Large Latte - Vanilla - 3.5"
#     parsed = parse_items(items_column)
#     assert len(parsed) == 2  # Two items
#     assert parsed[0]["item_name"] == "Coffee"  # Correct parsing
#     assert parsed[1]["variant"] == "Vanilla"  # Correct variant extraction
#     assert parsed[1]["price"] == 3.5  # Correct price conversion

def test_parse_items_invalid():
    items_column = "This is not valid"
    parsed = parse_items(items_column)
    assert len(parsed) == 0  # No matches

# def test_prepare_data():
#     raw_data = [
#         {
#             "timestamp": "2024-04-21 09:00:00",
#             "location": "Edinburgh",
#             "items": "Regular Coffee - - 2.5, Large Latte - Vanilla - 3.5",
#             "total_cost": "10.00",
#             "payment_method": "Cash"
#         }
#     ]
#     prepared = prepare_data(raw_data)
#     assert len(prepared) == 1  # Ensure single row processed
#     assert prepared[0]["total_cost"] == 10.0  # Total cost converted to float
#     assert prepared[0]["items"][0]["item_name"] == "Coffee"  # Correct parsing of items

def test_validate_data():
    data = [
        {
            "timestamp": "2024-04-21 09:00:00",
            "location": "Edinburgh",
            "items": "Regular Coffee - - 2.5",
            "total_cost": "10.00",
            "payment_method": "Cash"
        },
        {
            "timestamp": "",  # Missing timestamp
            "location": "Edinburgh",
            "items": "Regular Coffee - - 2.5",
            "total_cost": "10.00",
            "payment_method": "Cash"
        }
    ]
    valid_data, invalid_data = validate_data(data)
    assert len(valid_data) == 1
    assert len(invalid_data) == 1

@patch("builtins.open", new_callable=mock_open)
def test_save_data_to_json(mock_file):
    data = [{"key": "value"}]
    save_data_to_json(data, "dummy.json")
    mock_file.assert_called_once_with("dummy.json", 'w', encoding='utf-8')
    written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
    assert json.loads(written_data) == data
