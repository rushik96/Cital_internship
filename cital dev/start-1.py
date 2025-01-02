import requests 
import json

url = "http://localhost:11434/api/generate"

data ={
    "model" : "llama3.2",
    "prompt" : """You are an expert in inventory management for construction materials. I will provide you with a list of items in my inventory and a raw customer order.

Your task is to generate a JSON output where:

Keys are VUIDs from the inventory.
Values are objects with two fields:
name (the item name)
qty (the quantity requested by the customer).
Rules:

Ambiguous Items: If the customer order includes items with multiple matching variations in the inventory (e.g., "Shoes" without size), include all matching inventory items with their respective VUIDs, names, and null for the quantity.
Unspecific Orders: If the customer orders a general category (e.g., "Shoes"), include all items in that category from the inventory with their VUIDs, names, and null for the quantity.
Specific Orders: If the customer orders a specific item with a quantity (e.g., "Safety Shoes x 7"), include the matching inventory item(s) with their VUIDs, names, and the specified quantity.
Non-Matching Items: If an item in the customer order does not match any item in the inventory, do not include it in the output.
Example Inventory:

| Name                                          | VUID      |
|-----------------------------------------------|----------|
| Safetap Apollo PVC Safety Shoes (6 no)         | CP-023470-1 |
| Safetap Apollo PVC Safety Shoes (7 no)         | CP-023470-2 |
| Metal/Steel Cutting Blade  (Size: 14 inch)      | CP-218683-2 |
| Spades/Pawda Regular 8 No. without Handle  (Size: 8 no.) | CP-522929-1 |
| Bitumen (Damar) 9015                          | CP-058941-1 |
| Wooden Taar/Wire Brush                        | CP-038739-1 |
| Kantan Hessian Cloth / Jute Brown (Width 1 Meter) | CP-049621-1 |
| Measuring Tape (Steel) (5 meter)              | CP-796865-1 |
| Measuring Tape (Steel) (30 meter)             | CP-796865-2 |
| 16 AMP 5 Pin 3 Phase Industrial Plug          | CP-968013-1 |
| Shovel with Handle                            | CP-740924-1 |

Customer Order:

Ronark buildwell

Site- alankar (sanand)

Shoes
Pawda no handle x 5
Damar x 5 box"""
}

response = requests.post(url, json=data , stream=True)

# check the response status 
if response.status_code == 2000:
    print("Generated Text:", end=" ", flush=True)
    # Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            # Decode the line and parse the JSON
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)
            # Get the text from the response
            generated_text = result.get("response", "")
            print(generated_text, end="", flush=True)
else:
    print("Error:", response.status_code, response.text)