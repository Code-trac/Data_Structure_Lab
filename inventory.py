inventory = []

def add_item(item):
    sku = input("Enter SKU for the item: ")
    item['sku'] = sku
    #Checking for same or existing SKU
    for existing_item in inventory: 
        if existing_item['sku'] == sku:                
            print(f"Item with SKU {sku} already exists in the inventory.")
            return
    
    prod_name = input("Enter product name: ")
    # Validating product name
    if not prod_name.strip():
        print("Product name cannot be empty.")
        return
    # Validating price and quantity
    try:
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        total_price = price * quantity
        item['name'] = prod_name
        item['price'] = price
        item['quantity'] = quantity
        item['total_price'] = total_price
    except ValueError:
        print("Invalid price. Please enter a numeric value.")
        return
    
    product = {
        'sku': sku,
        'name': prod_name,
        'price': price,
        'quantity': quantity,
        'total_price': total_price
    }

    inventory.append(product)
    print(f"Item {prod_name} with SKU {sku} added to inventory.")

def display_inventory():
    if not inventory:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    for item in inventory:
        print(f"SKU: {item['sku']}, Name: {item['name']}, Price: ${item['price']:.2f}, Quantity: {item['quantity']}, Total Price: ${item['total_price']:.2f}")
    print()

#search by sku
def search():
    #search by sku
    sku = input("Enter SKU to search: ")
    for item in inventory:
        if item['sku'] == sku:
            print(f"Item found: SKU: {item['sku']}, Name: {item['name']}, Price: ${item['price']:.2f}, Quantity: {item['quantity']}, Total Price: ${item['total_price']:.2f}")
            return
    print(f"No item found with SKU: {sku}")
    #search by name
    name = input("Enter product name to search: ").lower()
    found = False
    for item in inventory:
        if item['name'].lower() == name:
            print(f"Item found: SKU: {item['sku']}, Name: {item['name']}, Price: ${item['price']:.2f}, Quantity: {item['quantity']}, Total Price: ${item['total_price']:.2f}")
            found = True
    if not found:
        print(f"No item found with name: {name}")

def delete_item():
    sku = input("Enter SKU of the item to delete: ")
    for item in inventory:
        if item['sku'] == sku:
            inventory.remove(item)
            print(f"Item with SKU {sku} has been deleted from the inventory.")
            return
    print(f"No item found with SKU: {sku}")


'''
Decrease stock of specific SKU based on sales.
 If SKU not found, notify user.
 If stock is insufficient, notify user.

 Args:
 inventory (list of tuples): [(SKU, quantity), ...]
 sku (int): SKU identifier to process sale
 qty_sold (int): Quantity sold
 Returns:
 updated_inventory (list of tuples) 
'''


def process_sale(inventory, sku, qty_sold):

    for item in inventory:
        if item['sku'] == sku:
            if item['quantity'] >= qty_sold:
                item['quantity'] -= qty_sold
                item['total_price'] = item['price'] * item['quantity']
                print(f"Sale processed. Updated quantity of SKU {sku}: {item['quantity']}")
                return inventory
            else:
                print(f"Insufficient stock for SKU {sku}. Available: {item['quantity']}, Requested: {qty_sold}")
                return inventory
    print(f"No item found with SKU: {sku}")
    return inventory

def identify_zero_stock_items(inventory):
    zero_stock = [item for item in inventory if item['quantity'] == 0]
    if not zero_stock:
        print("No items with zero stock.")
    else:
        print("Items with zero stock:")
        for item in zero_stock:
            print(f"SKU: {item['sku']}, Name: {item['name']}")


def main():
    while True:
        print("1. Add Item")
        print("2. Display Inventory")
        print("3. Search Item")
        print("4. Exit")
        print("5. Delete Item")
        print("6. Process Sale")
        choice = input("Enter your choice: ")

        if choice == '1':
            item = {}
            add_item(item)
        elif choice == '2':
            display_inventory()
        elif choice == '3':
            search()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            sku = input("Enter SKU to process sale: ")
            try:
                qty_sold = int(input("Enter quantity sold: "))
                process_sale(inventory, sku, qty_sold)
            except ValueError:
                print("Invalid quantity. Please enter a numeric value.")
            
            zero_stock = identify_zero_stock_items(inventory)
        elif choice == '4':
            print("Exiting the program.")
            break


        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
