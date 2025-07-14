import tkinter as tk
import backend

food_donations = []
money_donations = []
food_distribution = []

inventory=backend.load_data(backend.INVENTORY_FILE)
donations_log = backend.load_data(backend.DONATIONS_FILE)
distributions_log = backend.load_data(backend.DISTRIBUTIONS_FILE)

# Button Functions
def add_food():
    item = food_entry.get()
    try:
        quantity = int(food_quantity_entry.get())
    except:
        print("Could not change to an int")
    donor = food_donor_entry.get()
    if item and quantity and donor:
        backend.add_food_donation(inventory=inventory, donations_log=donations_log, donor_name="TEST", item_name=item, quantity=quantity, expiration_date=("2000-01-01"))
    
def add_money():
    try:
        amount = float(money_entry.get())
    except:
        print("Could not change amount to a float.")
    donor = money_donor_entry.get()
    if amount and donor:
        backend.add_money_donation(donations_log=donations_log, donor_name=donor, amount=amount)

def record_distribution():
    household = household_entry.get()
    item = distribute_item_entry.get()
    try:
        quantity = int(distribute_quantity_entry.get())
    except:
        print("Could not change to an int.")
    if household and item and quantity:
        backend.record_distribution(inventory=inventory, distributions_log=distributions_log, household_name=household, item_name=item, quantity_taken=quantity)

def view_distributions_inventory():
  # Creates a new popup window
    log_window = tk.Toplevel(root)
    log_window.title("Donation Logs")
    log_window.geometry("200x400")
    #backend.load_data(inventory)
    tk.Label(log_window, text="Food Donations", font=("Arial", 10, "bold")).pack(pady=5)
    #Adds label with data from the food, money, and distributions lists
    for donor, item, qty in food_donations:
        tk.Label(log_window, text=f"{donor}: {qty} of {item}").pack(anchor="w")
    tk.Label(log_window, text="Money Donations", font=("Arial", 10, "bold")).pack(pady=5)
    for donor, amount in money_donations:
        tk.Label(log_window, text=f"{donor}: ${amount}").pack(anchor="w")
    tk.Label(log_window, text="Distributions", font=("Arial", 10, "bold")).pack(pady=5)
    for household, item, qty in food_distribution:
        tk.Label(log_window, text=f"{household}: {qty} of {item}").pack(anchor="w")
    #for item in backend.output:
    #    tk.Lavel(log_window, text=backend.output[item], font=("Arial", 10, "bold")).pack(pady=5)



# GUI

root = tk.Tk()
root.title("Food Pantry App")
root.geometry("250x600")


# FOOD DONATION LABELS, ENTRY BOXES, AND BUTTONS

# Food donation labels
tk.Label(root, text="Food Donation", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2,
                                                                      padx=10, pady=5)
tk.Label(root, text="Donor Name:").grid(row=1, column=0, sticky="e")

# Food donation entry box
food_donor_entry = tk.Entry(root)
food_donor_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Food item label
tk.Label(root, text="Item:").grid(row=2, column=0, sticky="e")

# Food item entry box
food_entry = tk.Entry(root)
food_entry.grid(row=2, column=1, padx=10, pady=10)

# Food amount label
tk.Label(root, text="Amount:").grid(row=3, column=0, sticky="e")

# Food amount entry box
food_quantity_entry = tk.Entry(root)
food_quantity_entry.grid(row=3, column=1, padx=10, pady=10)

# Food donation add button, command = add_food
tk.Button(root, text="Add Food Donation", command=add_food).grid(row=4, column=0,
                                                             columnspan=2, pady=5)

# MONEY DONATION LABELS, ENTRY BOXES, AND BUTTONS

# Money donation labels
tk.Label(root, text="Money Donation", font=("Arial", 10, "bold")).grid(row=5, column=0,
                                                                       columnspan=2, padx=10, pady=5)
tk.Label(root, text="Donor Name:").grid(row=6, column=0, sticky="e")

# Money donation entry box
money_donor_entry = tk.Entry(root)
money_donor_entry.grid(row=6, column=1, pady=10)

# Money donation amount labels
tk.Label(root, text="Amount ($):").grid(row=7, column=0, sticky="e")

# Money donation entry box
money_entry = tk.Entry(root)
money_entry.grid(row=7, column=1, pady=10)

# Money donation button, command = add_money
tk.Button(root, text="Add Money Donation", command=add_money).grid(row=8, column=0,
                                                              columnspan=2, pady=5)

# FOOD DISTRIBUTION LABELS, ENTRY, AND BUTTONS

# Distribution labels
tk.Label(root, text="Food Distribution", font=("Arial", 10, "bold")).grid(row=9, column=0,
                                                                          columnspan=2, padx=10, pady=5)
tk.Label(root, text="Household:").grid(row=10, column=0, sticky="e")

# Distribution entry box
household_entry = tk.Entry(root)
household_entry.grid(row=10, column=1, pady=10)

# Item label and entry box
tk.Label(root, text="Item:").grid(row=11, column=0, sticky="e")
distribute_item_entry = tk.Entry(root)
distribute_item_entry.grid(row=11, column=1, pady=10)

# Amount label and entry box
tk.Label(root, text="Quantity:").grid(row=12, column=0, sticky="e")
distribute_quantity_entry = tk.Entry(root)
distribute_quantity_entry.grid(row=12, column=1, pady=10)

# Button to record distributions, command = record_distribution
tk.Button(root, text="Record Distribution", command=record_distribution).grid(row=13, column=0,
                                                               columnspan=2, pady=5)

# Button to view distributions, command = view_distributions_inventory
tk.Button(root, text="View Inventory & Distributions", command=view_distributions_inventory).grid(row=14, column=0,
                                                              columnspan=2, pady=10)

#tk.Button(root, text="View Inventory & Distributions", command=backend.view_inventory(backend.INVENTORY_FILE)).grid(row=14, column=0,
#                                                              columnspan=2, pady=10)

root.mainloop()