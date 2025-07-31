# St. Basil Food Pantry Management System
## Overview
This project is a desktop application designed to help non-profit food pantry organizers such as St. Basil Food Pantry to manage its operations. It provides a graphical interface for logging food, donations, tracking, and recording food distributions to households. The system is built with Python and the Tkinter library for the GUI.

## Features
* **Donation Logging**: Forms for logging both food and money donations. The food donation system supports adding multiple items in a single transaction.

* **Household Queue**: A waiting list to sign in and manage households as they arrive.

* **Live Distribution**: A "shopping cart" system for recording the distribution of multiple items to a household, with inventory search.

* **Data Persistence**: All data is saved to local JSON files, so information is not lost when the application is closed.

* **Data Visualization**: A simple bar graph shows the most frequently distributed items, valuable insights for pantry organizers.

## File Structure
* `main.py`: The main entry point to run the application.

* `app_gui.py`: Contains all the code for the graphical user interface (GUI), built with Tkinter by our front-end.

* `pantry_manager.py`: The "brain" of the application. It contains all the backend logic for managing data and operations.

* `pantry_models.py`: Acts only as data for the application, such as InventoryItem, Donation, and Household.

* `*.json`: These files (inventory.json, donations.json, distributions.json) act as the local database for the application.

## Requirements
The application is built using standard Python libraries. However, some feature requires an external library:

* **matplotlib:**
```pip install matplotlib```
* **Pillow:**
```pip install Pillow```

## Setup & Running
Follow these steps to get the application running on your system.

**1. Python:**
Ensure you have Python 3.x installed on your machine.

**3. Run the Application:**
Navigate to the project's root directory in your terminal and run the main.py file:

`python main.py`
## Test Data
This project includes sample data files (inventory.json, donations.json, distributions.json) to show the application's features immediately.

To use the test data: Simply run the application as described above. The data will be loaded automatically.

To start with a clean slate: Before running the application for the first time, you can simply delete the three .json files. The application will automatically generate new empty ones when you first save data.