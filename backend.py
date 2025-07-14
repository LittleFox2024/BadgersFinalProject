import datetime
import json
import os

# Set the files we need.
INVENTORY_FILE = 'inventory.json'
DONATIONS_FILE = 'donations.json'
DISTRIBUTIONS_FILE = 'distributions.json'

def load_data(file_path):
    '''Load the file needed to get or store data'''
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(file_path, data):
    '''Save the data to the given file'''
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def add_food_donation(inventory, donations_log, donor_name, item_name, quantity, expiration_date):
    '''Add food donation information'''
    print(f"Processing food donation from {donor_name}...")

    item_found = False
    for item in inventory:
        if item['name'].lower() == item_name.lower() and item['expiration_date'] == expiration_date:
            item['quantity'] += quantity
            item_found = True
            break

    if not item_found:
        new_item = {
            'name': item_name,
            'quantity': quantity,
            'expiration_date': expiration_date
        }
        inventory.append(new_item)

    donation_record = {
        'donor': donor_name,
        'type': 'Food',
        'item_details': f"{quantity}x {item_name} (Expires: {expiration_date})",
        'date': "working in progress"
    }
    donations_log.append(donation_record)

    save_data(INVENTORY_FILE, inventory)
    save_data(DONATIONS_FILE, donations_log)
    print("Success. Inventory updated and donation logged.")

def add_money_donation(donations_log, donor_name, amount):
    '''Add money donation information'''
    print(f"Processing money donation from {donor_name}...")
    donation_record = {
        'donor': donor_name,
        'type': 'Money',
        'item_details': f"${amount:.2f}",
        'date': "working in progress"
    }
    donations_log.append(donation_record)
    save_data(DONATIONS_FILE, donations_log)
    print("Success. Money donation logged.")

def record_distribution(inventory, distributions_log, household_name, item_name, quantity_taken):
    '''Add distribution record to the file.'''
    print(f"Processing distribution to {household_name}...")

    item_found_in_inventory = False
    for item in inventory:
        if item['name'].lower() == item_name.lower():
            if item['quantity'] >= quantity_taken:
                item['quantity'] -= quantity_taken
                item_found_in_inventory = True

                distribution_record = {
                    'household': household_name,
                    'item_details': f"{quantity_taken}x {item_name}",
                    'date': "working in progress"
                }
                distributions_log.append(distribution_record)

                save_data(INVENTORY_FILE, inventory)
                save_data(DISTRIBUTIONS_FILE, distributions_log)
                print(f"Success. {quantity_taken}x {item_name} distributed to {household_name}.")
            else:
                print(f"Error: Not enough {item['name']} in stock. Only {item['quantity']} available.")
                return
            break

    if not item_found_in_inventory:
        print(f"Error: Item '{item_name}' not found in inventory.")

def view_inventory(inventory):
    '''Pulls the inventory info from the file'''
    print("\nCurrent Pantry Inventory:")
    if not inventory:
        print("Inventory is empty.")
    else:
        for item in inventory:
            if item['quantity'] > 0:
                print(f"- {item['name']}, Quantity: {item['quantity']}, Expires: {item['expiration_date']}")

def view_donations(donations_log):
    '''View all donations logged'''
    print("\nDonation Log:")
    if not donations_log:
        print("No donations logged.")
    else:
        for log in donations_log:
            print(f"- Date: {log['date']}, Donor: {log['donor']}, Type: {log['type']}, Details: {log['item_details']}")

def view_distributions(distributions_log):
    '''View all food distribution logged'''
    print("\nFood Distribution Log:")
    if not distributions_log:
        print("No distributions logged.")
    else:
        for log in distributions_log:
            print(f"- Date: {log['date']}, Household: {log['household']}, Items: {log['item_details']}")

def main():

    # Load the data
    inventory = load_data(INVENTORY_FILE)
    donations_log = load_data(DONATIONS_FILE)
    distributions_log = load_data(DISTRIBUTIONS_FILE)

    print("Pantry Backend Test Console")

    while True: ## This is a console view, may be removed later.
        print("\nMenu:")
        print("1. View Inventory")
        print("2. Log a Food Donation")
        print("3. Log a Money Donation")
        print("4. Record Food Distribution")
        print("5. View Donation Log")
        print("6. View Distribution Log")
        print("7. Exit")

        choice = input("Enter an option: ")

        if choice == '1':
            view_inventory(inventory)
        elif choice == '2':
            print("\nLog a Food Donation")
            donor = input("Enter donor's name: ")
            item = input("Enter item name: ")
            try:
                qty = int(input("Enter quantity: "))
            except ValueError:
                print("Invalid quantity. Please enter a whole number.")
                continue
            exp_date = input("Enter expiration date (YYYY-MM-DD): ")
            add_food_donation(inventory, donations_log, donor, item, qty, exp_date)
        elif choice == '3':
            print("\nLog a Money Donation")
            donor = input("Enter donor's name: ")
            try:
                amount = float(input("Enter amount: $"))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            add_money_donation(donations_log, donor, amount)
        elif choice == '4':
            print("\nRecord Food Distribution")
            household = input("Enter household name/ID: ")
            item = input("Enter item to distribute: ")
            try:
                qty = int(input("Enter quantity to give: "))
            except ValueError:
                print("Invalid quantity. Please enter a whole number.")
                continue
            record_distribution(inventory, distributions_log, household, item, qty)
        elif choice == '5':
            view_donations(donations_log)
        elif choice == '6':
            view_distributions(distributions_log)
        elif choice == '7':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == '__main__':
    main()