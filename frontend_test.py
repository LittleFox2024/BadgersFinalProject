import tkinter as tk

food_donations = []
money_donations = []
food_distribution = []

# MOCK FUNCTIONS
def add_food():
    item = food_entry.get()
    quantity = food_quantity_entry.get()
    donor = food_donor_entry.get()
    if item and quantity and donor:
      # Adds to food_donations list
        food_donations.append((donor, item, quantity))
      # Deletes previous entries from entry box
        food_entry.delete(0, tk.END)
        food_quantity_entry.delete(0, tk.END)
        food_donor_entry.delete(0, tk.END)

def add_money():
    amount = money_entry.get()
    donor = money_donor_entry.get()
    if amount and donor:
        money_donations.append((amount, donor))
        money_entry.delete(0, tk.END)
        money_donor_entry.delete(0,tk.END)

def record_distribution():
    household = household_entry.get()
    item = distribute_item_entry.get()
    quantity = distribute_quantity_entry.get()
    if household and item and quantity:
        food_distribution.append((household, item, quantity))
        household_entry.delete(0, tk.END)
        distribute_item_entry.delete(0, tk.END)
        distribute_quantity_entry.delete(0, tk.END)

def view_distributions_inventory():
  # Creates a new popup window
    log_window = tk.Toplevel(root)
    log_window.title("Donation Logs")
    log_window.geometry("200x400")
    tk.Label(log_window, text="Food Donations", font=("Arial", 10, "bold")).pack(pady=5)
  # Adds label with data from the food, money, and distributions lists
    for donor, item, qty in food_donations:
        tk.Label(log_window, text=f"{donor}: {qty} of {item}").pack(anchor="w")
    tk.Label(log_window, text="Money Donations", font=("Arial", 10, "bold")).pack(pady=5)
    for donor, amount in money_donations:
        tk.Label(log_window, text=f"{donor}: ${amount}").pack(anchor="w")
    tk.Label(log_window, text="Distributions", font=("Arial", 10, "bold")).pack(pady=5)
    for household, item, qty in food_distribution:
        tk.Label(log_window, text=f"{household}: {qty} of {item}").pack(anchor="w")



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

root.mainloop()






