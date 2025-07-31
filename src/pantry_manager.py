# Design Rationale:
#
# To the team: I've chosen to structure our backend using a "Manager" class
# since it will make our project much easier to manage; other classes interacting with each other, etc.
# (I know it can get messy, but I feel structuring this way for this project will reduce difficulty).
# Here's the thinking:
#
# 1.  Our "Models"/Classes (like InventoryItem, Donation) in pantry_models.py
#     are simple data containers. Their only job is to hold information. They
#     don't know how to save to files or interact with other models. 
#     Its simple job of "being an item" gets complicated.
#
# 2.  This "PantryManager" class acts as the "brain" of the entire operations. It's
#     responsible for handling actions that involve multiple data objects.
#     For example, a distribution involves a Household and multiple InventoryItems. 
#
# Why this approach?
#   -   Easier to maintain (scalability?): If we change how we save data (moving
#       from JSON files to a real database), we only have to update this
#       one manager file. The models and the frontend UI won't need to change.

import json
import os
from datetime import date
from .pantry_models import InventoryItem, Donation, Household

class PantryManager:
    """
    Manages all data and operations for the food pantry.
    """
    def __init__(self, data_folder='data'):
        """
        Set up the file paths for our JSON database and trigger the initial
        loading of all data into the application's memory.
        """
        self.data_folder = data_folder
        self.inventory_file = os.path.join(self.data_folder, 'inventory.json')
        self.donations_file = os.path.join(self.data_folder, 'donations.json')
        self.distributions_file = os.path.join(self.data_folder, 'distributions.json')
        
        # Ensure the data directory exists
        os.makedirs(self.data_folder, exist_ok=True)

        self._load_all_data()
        
        # The household queue is not saved between
        # sessions. This is because a waiting list is only relevant for the current day.
        self.household_queue = []
        self._next_household_id = 1

    def _load_all_data(self):
        """
        This method is for reading the raw data from the
        JSON files and transforming it into the structured class objects
        (like InventoryItem) that our application uses internally.
        """
        inventory_data = self._read_json(self.inventory_file)
        self.inventory = []
        for data in inventory_data:
            item = InventoryItem(
                name=data['name'],
                quantity=data['quantity'],
                expiration_date=data['expiration_date']
            )
            self.inventory.append(item)

        donations_data = self._read_json(self.donations_file)
        self.donations_log = []
        for data in donations_data:
            # When we load a food donation, the 'details'
            # are just dictionaries. We must convert them back into InventoryItem
            # objects so the rest of our application can work with them consistently.
            donation_details = []
            if data['type'] == 'Food':
                for item_dict in data['details']:
                    item_obj = InventoryItem(**item_dict)
                    donation_details.append(item_obj)
            else:
                donation_details = data['details']

            donation = Donation(
                donor=data['donor'],
                donation_type=data['type'],
                details=donation_details,
                date=data['date']
            )
            self.donations_log.append(donation)
            
        self.distributions_log = self._read_json(self.distributions_file)

    def _read_json(self, file_path):
        """
        Safe helper method for reading JSON files. We use it to avoid
        crashing the application if a file is missing or empty on first run.
        """
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_data(self):
        """
        Writes the application's current data
        back to the JSON files, ensuring that all changes are persisted.
        """
        inventory_to_save = []
        for item in self.inventory:
            inventory_to_save.append(item.to_dict())
        with open(self.inventory_file, 'w') as f:
            json.dump(inventory_to_save, f, indent=4)

        donations_to_save = []
        for donation in self.donations_log:
            donations_to_save.append(donation.to_dict())
        with open(self.donations_file, 'w') as f:
            json.dump(donations_to_save, f, indent=4)
            
        with open(self.distributions_file, 'w') as f:
            json.dump(self.distributions_log, f, indent=4)

    def add_food_donation(self, donor_name, food_item_data):
        """
        Handles the logic for a food donation. It's responsible for both
        updating the inventory levels and creating a record of the donation event.
        """
        donated_items = []
        for item_data in food_item_data:
            item = InventoryItem(
                name=item_data['name'],
                quantity=item_data['quantity'],
                expiration_date=item_data['expiration_date']
            )
            donated_items.append(item)
        
        # This logic prevents duplicate items. If a donated item already
        # exists in the inventory, we just increase its quantity.
        for new_item in donated_items:
            item_found = False
            for existing_item in self.inventory:
                if (existing_item.name.lower() == new_item.name.lower() and
                    existing_item.expiration_date == new_item.expiration_date):
                    existing_item.quantity += new_item.quantity
                    item_found = True
                    break
            if not item_found:
                self.inventory.append(new_item)
        
        donation = Donation(donor_name, 'Food', donated_items, date.today().isoformat())
        self.donations_log.append(donation)
        self._save_data()
        return donation

    def add_money_donation(self, donor_name, amount):
        """Handles the simpler case of logging a monetary donation."""
        donation = Donation(donor_name, 'Money', amount, date.today().isoformat())
        self.donations_log.append(donation)
        self._save_data()
        return donation

    def sign_in_household(self, household_name, household_size):
        """
        Adds a household to the waiting queue and assigns it a
        unique, sequential ID for the current session.
        """
        household = Household(self._next_household_id, household_name, household_size)
        self.household_queue.append(household)
        self._next_household_id += 1
        return household

    def remove_household_from_queue(self, household_id):
        """
        Provides a way to remove a household from the queue, which is
        necessary for cases where a family might leave before being served.
        """
        household_to_remove = None
        for h in self.household_queue:
            if h.id == int(household_id):
                household_to_remove = h
                break
        
        if household_to_remove:
            self.household_queue.remove(household_to_remove)
        else:
            raise ValueError(f"Could not find household with ID {household_id} to remove.")

    def record_distribution(self, household_id, items_taken_data):
        """
        Handles the core logic of a distribution. It validates that we have
        enough stock, updates the inventory, logs the event, and removes
        the household from the queue.
        """
        household = None
        for h in self.household_queue:
            if h.id == int(household_id):
                household = h
                break
        
        if not household:
            raise ValueError(f"Household with ID {household_id} not found in queue.")

        # Before we change any data,
        # we first check if all requested items are in stock. This prevents
        # a "partial" distribution where some items are given but others aren't.
        for item_taken in items_taken_data:
            item_in_stock = None
            for i in self.inventory:
                if i.name.lower() == item_taken['name'].lower():
                    item_in_stock = i
                    break
            
            if not item_in_stock:
                raise ValueError(f"Item {item_taken['name']} not found in inventory.")
            if item_in_stock.quantity < item_taken['quantity']:
                raise ValueError(f"Insufficient stock for {item_taken['name']}.")
            
            item_in_stock.quantity -= item_taken['quantity']
        
        distribution_record = {
            'household_name': household.name,
            'household_size': household.size,
            'items': items_taken_data,
            'date': date.today().isoformat()
        }
        self.distributions_log.append(distribution_record)
        self.household_queue.remove(household)
        self._save_data()
        return distribution_record

    def get_inventory(self):
        return self.inventory
        
    def get_queue(self):
        return self.household_queue

    def get_pantry_status(self):
        """Provides a quick summary of key metrics for the main menu display."""
        return {
            'households_waiting': len(self.household_queue),
            'unique_items_in_inventory': len([item for item in self.inventory if item.quantity > 0])
        }

    def get_analytics_data(self):
        """
        Processes the raw distribution log to provide
        data suitable for creating a graph.
        """
        item_counts = {}
        for record in self.distributions_log:
            for item in record['items']:
                name = item['name']
                quantity = item['quantity']
                item_counts[name] = item_counts.get(name, 0) + quantity
        
        # Sorting the data here means the UI doesn't have to. The manager
        # provides the data ready to display.
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_items)
