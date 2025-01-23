import unittest
import os
from datetime import datetime
from normalise_data import (
    normalize_branches,
    normalize_transactions,
    normalize_products,
    normalize_product_transactions,
    save_data_to_json,
    save_data_to_csv,
    load_json_data
) # loading in all the functions contained in the python files

class TestNormalisation(unittest.TestCase):
    def test_normalize_branches(self): 
        data = [{"branch_name":"sample"}] # sample input for the test to try
        expected_output = [
            {
                "branch_id":1,
                "name": "Edinburgh",
                "location": "Edinburgh"
            }
        ]
        self.assertEqual(normalize_branches(data), expected_output)
        # Test that the function returns the expected output

    def test_normalize_transactions(self):
        data = [
            {
                "timestamp": "01/01/2024 10:00",
                "total_cost": 100.0,
                "payment_method": "card"
            }
        ]

        expected_output = [
            {
                "payment_id": 1,
                "branch_id": 1,  # Assuming all transactions are from Edinburgh
                "timestamp": datetime(2024, 1, 1, 10, 0),
                "total_amount": 100.0,
                "payment_method": "card"
            }
        ]
        self.assertEqual(normalize_transactions(data), expected_output)
    
    # def test_normalize_products(self):
    #     data = [
    #         {"items":[
    #             {
    #                 "item_name": "Shirt",
    #                 "variant": "Red",
    #                 "size": "L",
    #                 "price": 25.0
    #                    }
    #                 ]
    #             }
    #         ]
    #     expected_output = [
    #         {
    #             "product_id": 1,
    #             "item_name": "Shirt",
    #             "variant": "Red",
    #             "size": "L",
    #             "price": 25.0
    #         }
    #     ]
    #     self.assertEqual(normalize_products(data), expected_output)

    
    # def test_normalize_product_transactions(self):
    #     data = [
    #         {"items":[{"item_name": "Shirt",
    #                    "variant": "Red",
    #                    "size": "L",
    #                    "price": 25.0}]
    #             }
    #         ]
    #     products = [
    #         {   
    #             "product_id": 1,
    #             "item_name": "Shirt",
    #             "variant": "Red",
    #             "size": "L",
    #             "price": 25.0
    #         }
    #         ]
    #     expected_outcome = [
    #         {
    #             "product_transactions_id": 1,
    #             "payment_id": 1,
    #             "product_id": 1,
    #             "quantity": 1
    #         }
    #     ]
    #     self.assertEqual(normalize_product_transactions(data, products), expected_outcome)
    #     # Testing that the function appends the right information properly

    def test_save_data_to_json(self): # Here we are making use of both save_data_to_json & load_json_data
        data = [{"key": "value"}]
        file_path = "test.json"
        save_data_to_json(data, file_path)
        loaded_data = load_json_data(file_path)
        self.assertEqual(loaded_data, data)
        os.remove(file_path)

    def test_save_data_to_csv(self):
        data = [{'key':'value'}]
        file_path = "test.csv"
        save_data_to_csv(data,file_path)
        with open (file_path, "r") as file:
            content = file.readlines()
        expected_content = ["key\n", "value\n"]
        self.assertEqual(content, expected_content)
        os.remove(file_path)

if __name__ == "__main__":
        unittest.main()