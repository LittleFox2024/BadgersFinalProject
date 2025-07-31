class InventoryItem:
    """Represents a single item in the pantry's inventory."""
    def __init__(self, name, quantity, expiration_date):
        self.name = name
        self.quantity = int(quantity)
        self.expiration_date = expiration_date

    def to_dict(self):
        """Converts the InventoryItem object into a dictionary."""
        return {
            'name': self.name,
            'quantity': self.quantity,
            'expiration_date': self.expiration_date
        }

class Donation:
    """Represents a single donation event (either food or money)."""
    def __init__(self, donor, donation_type, details, date):
        self.donor = donor
        self.type = donation_type # This will be either 'Food' or 'Money'
        self.details = details    # For 'Food', this is a list of InventoryItem objects.
                                  # For 'Money', this is just a number (the amount).
        self.date = date

    def to_dict(self):
        """
        Converts the Donation object into a dictionary so it can be saved
        as JSON. This method handles the two different types of donations.
        """
        if self.type == 'Food':
            # If it's a food donation, we know 'self.details' is a list of
            # InventoryItem objects. We need to loop through this list.
                        
            items_as_dicts = []
            
            # For each InventoryItem object in our details list...
            for item_object in self.details:
                # ...call its own .to_dict() method to convert it...
                item_dict = item_object.to_dict()
                items_as_dicts.append(item_dict)
                
            details_to_save = items_as_dicts
            
        else: # This handles the 'Money' donation case.
            # If it's a money donation, 'self.details' is just a number.
            # We can use it directly without any conversion.
            details_to_save = self.details
            
        # Return the final dictionary for the entire Donation object.
        return {
            'donor': self.donor,
            'type': self.type,
            'details': details_to_save,
            'date': self.date
        }

class Household:
    """Represents a household waiting in the queue."""
    def __init__(self, household_id, name, size):
        self.id = household_id
        self.name = name
        self.size = int(size)
