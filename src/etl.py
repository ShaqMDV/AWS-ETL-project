import csv
from datetime import datetime
import logging
import re
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

COLUMN_NAMES = ['timestamp', 'location', 'customer_name', 'items', 'total_cost', 'payment_method', 'credit_card']

def extract(body_text):
    LOGGER.info('extract: starting')
    reader = csv.DictReader(
        body_text,
        fieldnames=COLUMN_NAMES,
        delimiter=',',
    )

    # skip header row
    next(reader)

    data = [row for row in reader]

    LOGGER.info(f'extract: done: rows={len(data)}')
    return data
 
# Transformation functions
def parse_items(items_column):
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
def transform(data):
    LOGGER.info('transform: starting')
    for row in data:
        row["items"] = parse_items(row.get("items", ""))
        row["total_cost"] = float(row.get("total_cost", 0.0))
        row["timestamp"] = datetime.strptime(row["timestamp"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        row.pop("credit_card", None)  # Remove sensitive information
        row.pop("customer_name", None)  # Remove customer name
    LOGGER.info(f'transform: done: rows={len(data)}')
    return data

# Normalization functions
def normalize(data):
    """
    Normalize transformed data into relational tables.
    :param data: Transformed data
    :return: Dictionary of normalized tables
    """
    LOGGER.info('normalize: starting')
    branches = []
    branch_map = {}  # To map branch names to unique branch IDs
    transactions = []
    products = {}
    product_transactions = []

    for i, row in enumerate(data, start=1):
        # Extract branch information dynamically
        branch_name = row.get("location", "Unknown")
        if branch_name not in branch_map:
            branch_id = len(branches) + 1
            branch_map[branch_name] = branch_id
            branches.append({"branch_id": branch_id, "name": branch_name, "location": branch_name})

        branch_id = branch_map[branch_name]

        # Normalize transactions
        transactions.append({
            "payment_id": i,
            "branch_id": branch_id,
            "timestamp": row["timestamp"],
            "total_amount": row["total_cost"],
            "payment_method": row["payment_method"]
        })

        # Normalize products and product transactions
        for item in row["items"]:
            product_key = (item["item_name"], item["variant"], item["size"], item["price"])
            if product_key not in products:
                products[product_key] = {
                    "product_id": len(products) + 1,
                    "name": item["item_name"],
                    "variant": item["variant"],
                    "size": item["size"],
                    "price": item["price"]
                }
            product_transactions.append({
                "product_transactions_id": len(product_transactions) + 1,
                "payment_id": i,
                "product_id": products[product_key]["product_id"],
                "quantity": 1  # Assuming quantity is 1 for simplicity
            })

    # Debug log to verify branch data
    LOGGER.debug(f'Branches: {branches}')

    LOGGER.info('normalize: done')
    return {
        "branches": branches,
        "transactions": transactions,
        "products": list(products.values()),
        "product_transactions": product_transactions
    }

