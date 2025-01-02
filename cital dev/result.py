
import json
from collections import defaultdict

# Example Inventory data structure
inventory = {
    "Shoes": [
        {"VUID": "CP-023470-1", "Name": "Safetap Apollo PVC Safety Shoes (6 no)"},
        {"VUID": "CP-023470-2", "Name": "Safetap Apollo PVC Safety Shoes (7 no)"},
    ],
    "Pawda": [
        {"VUID": "CP-522929-1", "Name": "Spades/Pawda Regular 8 No. without Handle  (Size: 8 no.)"}
    ],
    "Bitumen": [
        {"VUID": "CP-058941-1", "Name": "Bitumen (Damar) 9015"}
    ],
    "Brushes": [
        {"VUID": "CP-038739-1", "Name": "Wooden Taar/Wire Brush"},
        {"VUID": "CP-049621-1", "Name": "Kantan Hessian Cloth / Jute Brown (Width 1 Meter)"}
    ],
    "Measuring Tapes": [
        {"VUID": "CP-796865-1", "Name": "Measuring Tape (Steel) (5 meter)"},
        {"VUID": "CP-796865-2", "Name": "Measuring Tape (Steel) (30 meter)"}
    ],
    "Electrical Plug": [
        {"VUID": "CP-968013-1", "Name": "16 AMP 5 Pin 3 Phase Industrial Plug"}
    ],
    "Shovels": [
        {"VUID": "CP-740924-1", "Name": "Shovel with Handle"}
    ]
}

# Customer Order data structure
customer_order = {
    "Ronark buildwell": {
        "Site- alankar (sanand)": {
            "Shoes": 5,
            "Pawda no handle": 5,
            "Damar": 5,
            "Box (Note: Box size is assumed to be the same as the quantity):"  1,
        }
    }
}

# Function to process customer order and generate output
def process_customer_order(inventory, customer_order):
    output = {}
    
    for site_name, orders in customer_order["Ronark buildwell"].items():
        for product_name, quantity in orders.items():
            product_name = product_name.replace("x ", "")
            
            if product_name not in inventory:
                continue
            
            products = inventory[product_name]
            
            # Process Shoes
            if product_name == "Shoes":
                shoe_products = [item for item in products if "no" in item["Name"]]
                
                if len(shoe_products) > 1:  # Ambiguous Items
                    output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"]} for product in products]
                    
                elif shoe_products and (int(product["Name"].split("no")[0].strip()) <= quantity or len(shoe_products) == 1):
                    if shoe_products:
                        output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"]}]
                        for item in products:
                            if int(item["Name"].split("no")[0].strip()) > quantity:
                                output[product_name]["VUID"] += f", {item['VUID']}"
                    else:
                        # Unspecific Orders
                        category = [category for category in inventory.keys() if product_name.lower() in category.lower()][0]
                        products_in_category = [item for item in products if int(item["Name"].split("no")[0].strip()) > 0]
                        
                        output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"]} for product in products_in_category]
                elif shoe_products:
                    # Specific Orders
                    output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"], "qty": quantity}]
                    
            else:  # Process Pawda
                pawda_products = [item for item in products if product_name == item["Name"] and int(item["Name"].split("no")[1].strip()) <= quantity]
                
                if len(pawda_products) > 1:
                    output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"]} for product in products]
                    
                elif pawda_products and len(pawda_products) == 1:
                    output[product_name] = [{"VUID": pawda_products[0]["VUID"], "Name": pawda_products[0]["Name"], "qty": quantity}]
                
            # Process Bitumen
            if product_name == "Bitumen":
                bitumen_product = [item for item in products if int(item["Name"].split(" ")[1]) <= quantity]
                
                if len(bitumen_product) > 1:
                    output[product_name] = [{"VUID": product["VUID"], "Name": product["Name"]} for product in products]
                    
                elif bitumen_product and len(bitumen_product) == 1:
                    output[product_name] = [{"VUID": bitumen_product[0]["VUID"], "Name": bitumen_product[0]["Name"], "qty": quantity}]
                
            return json.dumps(output, indent=4)

    # If no products were found in the inventory, return an empty JSON object
    return json.dumps({}, indent=4)


# Call the function and print the result
result = process_customer_order(inventory, customer_order)
print(result)
