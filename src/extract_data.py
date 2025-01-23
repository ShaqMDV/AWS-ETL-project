import csv
import json
import re


COLUMN_NAMES = ["timestamp", "location", "customer_name", "items", "total_cost", "payment_method", "credit_card"]


# Function to save data as JSON
def save_data_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")


# Function to parse items column
def parse_items(items_column):
        """
        Parses the items column into a structured list of items with name, size, variant (if present), and price.
        :param items_column: A string containing items, sizes, and prices.
        :return: A list of dictionaries with parsed item details.
        """
        parsed_items = []
        try:
            # Split items by comma
            items = items_column.split(',')
           
            # Regex to match items with or without a variant
            regex_with_variant = r"^(?P<size>\w+)\s+(?P<item_name>[a-zA-Z\s]+)\s+-\s+(?P<variant>[a-zA-Z\s]+)\s+-\s+(?P<price>[0-9.]+)$"
            regex_without_variant = r"^(?P<size>\w+)\s+(?P<item_name>[a-zA-Z\s]+)\s+-\s+(?P<price>[0-9.]+)$"
           
            for item in items:
                item = item.strip()                
                # Try to match with variant first
                match = re.match(regex_with_variant, item)
                if match:
                    parsed_items.append({
                        "item_name": match.group("item_name").strip(),
                        "variant": match.group("variant").strip(),
                        "size": match.group("size").strip(),
                        "price": float(match.group("price").strip())
                    })
                    continue
               
                # If no match, try without variant
                match = re.match(regex_without_variant, item)
                if match:
                    parsed_items.append({
                        "item_name": match.group("item_name").strip(),
                        "variant": None,  # No variant available
                        "size": match.group("size").strip(),
                        "price": float(match.group("price").strip())
                    })
                    continue
                else:
                # Log unmatched items
                    print(f"Item format not matched: {item}")
            return parsed_items
        except Exception as e:
            print(f"Error parsing items: {e}")        
        return parsed_items





def prepare_data(data):
   """
   Prepares the data in a structured format for further processing.
   Removes sensitive information and parses the items column.
   :param data: List of rows (dictionaries)
   :return: Processed data (list of cleaned dictionaries)
   """
   processed_data = []
   for row in data:
       try:
           cleaned_row = {
               "timestamp": row.get("timestamp", "").strip(),
               "location": row.get("location", "").strip(),
               "items": parse_items(row.get("items", "").strip()),  # Parse items column
               "total_cost": float(row.get("total_cost", "0").strip()),  # Convert to float
               "payment_method": row.get("payment_method", "").strip()
           }
           processed_data.append(cleaned_row)
       except Exception as e:
           print(f"Error processing row: {e}")
   return processed_data


# Function to read CSV
def read_csv(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=COLUMN_NAMES)
            data = [{key: value.strip() for key, value in row.items()} for row in reader]
        return data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None



# Function to validate data
def validate_data(data):
   """
   Validates the extracted data for missing or malformed entries.
   :param data: List of rows (dictionaries)
   :return: Tuple (valid_data, invalid_data)
   """
   valid_data = []
   invalid_data = []


   for row in data:
       # Check if all required fields are present and non-empty
       required_fields = ["timestamp", "location", "items", "total_cost", "payment_method"]
       if all(row.get(field, "").strip() for field in required_fields):
           valid_data.append(row)
       else:
           invalid_data.append(row)


   return valid_data, invalid_data


# Main execution block
if __name__ == "__main__":
   # Replace with the actual CSV file path in the data folder
   file_path = "../data/edinburgh_21-04-2024_09-00-00.csv"
   output_path = "../data/prepared_data.json"


   # Step 1: Read CSV
   raw_data = read_csv(file_path)
   if raw_data is not None:
       # Step 2: Validate Data
       valid_data, invalid_data = validate_data(raw_data)
       print(f"Valid Entries: {len(valid_data)}")
       print(f"Invalid Entries: {len(invalid_data)}")


       # Step 3: Prepare Data
       structured_data = prepare_data(valid_data)
       print(f"Prepared Data: {structured_data[:5]}")  # Show the first 5 rows


       # Step 4: Save Prepared Data
       save_data_to_json(structured_data, output_path)
