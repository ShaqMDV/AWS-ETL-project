import json
import csv
from datetime import datetime

# Normalization Functions
def normalize_branches(data):
   branches = [
       {
           "branch_id": 1,
           "name": "Edinburgh",
           "location": "Edinburgh"
       }
   ]
   return branches


def normalize_transactions(data):
   transactions = []
   for i, row in enumerate(data, start=1):
       transactions.append({
           "payment_id": i,
           "branch_id": 1,  # Assuming all transactions are from Edinburgh
           "timestamp": datetime.strptime(row["timestamp"], "%d/%m/%Y %H:%M"),
           "total_amount": row["total_cost"],
           "payment_method": row["payment_method"]
       })
   return transactions


def normalize_products(data):
   product_set = {}
   product_id = 1
   for row in data:
       for item in row["items"]:
           product_key = (item["item_name"], item["variant"], item["size"], item["price"])
           if product_key not in product_set:
               product_set[product_key] = {
                   "product_id": product_id,
                   "name": item["item_name"],
                   "variant": item["variant"],
                   "size": item["size"],
                   "price": item["price"]
               }
               product_id += 1
   return list(product_set.values())


def normalize_product_transactions(data, products):
   product_map = {
       (p["name"], p["variant"], p["size"], p["price"]): p["product_id"] for p in products
   }
   product_transactions = []
   product_transactions_id = 1
   for i, row in enumerate(data, start=1):  # i is the payment_id
       for item in row["items"]:
           product_key = (item["item_name"], item["variant"], item["size"], item["price"])
           product_transactions.append({
               "product_transactions_id": product_transactions_id,
               "payment_id": i,
               "product_id": product_map[product_key],
               "quantity": 1  # Assuming quantity = 1 for now
           })
           product_transactions_id += 1
   return product_transactions


# File Saving Functions
def save_data_to_json(data, file_path):
   """
   Saves the given data to a JSON file.
   :param data: The data to save (list of dictionaries).
   :param file_path: The path to save the JSON file.
   """
   def custom_serializer(obj):
       if isinstance(obj, datetime):
           return obj.strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as a string
       raise TypeError(f"Type {type(obj)} not serializable")


   try:
       with open(file_path, "w") as file:
           json.dump(data, file, indent=4, default=custom_serializer)
       print(f"Data successfully saved to {file_path} (JSON)")
   except Exception as e:
       print(f"Error saving JSON file: {e}")


def save_data_to_csv(data, file_path):
   """
   Saves the given data to a CSV file.
   :param data: The data to save (list of dictionaries).
   :param file_path: The path to save the CSV file.
   """
   try:
       with open(file_path, "w", newline="") as file:
           writer = csv.DictWriter(file, fieldnames=data[0].keys())
           writer.writeheader()
           writer.writerows(data)
       print(f"Data successfully saved to {file_path} (CSV)")
   except Exception as e:
       print(f"Error saving CSV file: {e}")


# Function to Load JSON Data
def load_json_data(file_path):
   """
   Loads JSON data from a file.
   :param file_path: Path to the JSON file.
   :return: Parsed JSON data.
   """
   try:
       with open(file_path, "r") as file:
           data = json.load(file)
       return data
   except Exception as e:
       print(f"Error loading JSON file: {e}")
       return None


# Main Test Block
if __name__ == "__main__":
   # Path to the prepared_data.json file
   json_file_path = "../data/prepared_data.json"


   # Load the data
   prepared_data = load_json_data(json_file_path)


   if prepared_data:
       # Normalize tables
       branches_table = normalize_branches(prepared_data)
       transactions_table = normalize_transactions(prepared_data)
       products_table = normalize_products(prepared_data)
       product_transactions_table = normalize_product_transactions(prepared_data, products_table)


       # File paths
       base_path = "../data/"
       file_names = {
           "branches": "branches",
           "transactions": "transactions",
           "products": "products",
           "product_transactions": "product_transactions",
       }


       # Save data as JSON
       save_data_to_json(branches_table, f"{base_path}{file_names['branches']}.json")
       save_data_to_json(transactions_table, f"{base_path}{file_names['transactions']}.json")
       save_data_to_json(products_table, f"{base_path}{file_names['products']}.json")
       save_data_to_json(product_transactions_table, f"{base_path}{file_names['product_transactions']}.json")


       # Save data as CSV
       save_data_to_csv(branches_table, f"{base_path}{file_names['branches']}.csv")
       save_data_to_csv(transactions_table, f"{base_path}{file_names['transactions']}.csv")
       save_data_to_csv(products_table, f"{base_path}{file_names['products']}.csv")
       save_data_to_csv(product_transactions_table, f"{base_path}{file_names['product_transactions']}.csv")
   else:
       print("Failed to load JSON data.")