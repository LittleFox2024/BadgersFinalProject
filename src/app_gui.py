import tkinter as tk
from tkinter import ttk, messagebox
from .pantry_manager import PantryManager

# These features are optional. If the libraries are not installed, the
# application will still run but without the icon or graph. This is a
# robust way to handle optional dependencies.
# To install: pip install Pillow matplotlib
try:
    from PIL import Image, ImageTk
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

BG_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
BUTTON_COLOR = "#f2f2f2"
ACTIVE_BUTTON_COLOR = "#d9d9d9"
FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 12
FONT_BOLD = (FONT_FAMILY, FONT_SIZE_LARGE, "bold")
FONT_NORMAL = (FONT_FAMILY, FONT_SIZE_NORMAL)

class AppGUI(tk.Tk):
    """
    The main GUI class for the pantry application. It inherits from tk.Tk
    to become the main window.
    """
    def __init__(self):
        super().__init__()
        
        # Basic Window Setup#
        self.title('St. Basil Food Pantry Management System')
        self.geometry('800x680')
        self.configure(bg=BG_COLOR)

        # Backend Initialization#
        self.pantry_manager = PantryManager()
        
        # UI State Variables#
        # These lists and dictionaries hold temporary data for the current
        # user session, like the items in a "shopping cart" before checkout.
        self.current_distribution_cart = {}
        self.current_donation_items = []

        # Configure Styles#
        self._configure_styles()

        # UI Creation#
        # We use a main container frame so we can easily switch between the
        # main menu and the detailed notebook view by showing one and hiding the other.
        self.main_container = ttk.Frame(self, style="Main.TFrame")
        self.main_container.pack(expand=True, fill='both')

        self._create_main_menu_view()
        self._create_notebook_view() 

        self.show_main_menu()

    def _configure_styles(self):
        """
        This method centralizes all the styling for our Tkinter widgets.
        It's good practice because it keeps the visual design separate
        from the application's structure.
        """
        style = ttk.Style(self)
        style.theme_use('clam') # 'clam' is a good base for custom styling.
        
        # General widget styles for the dark theme
        style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_NORMAL)
        style.configure("TFrame", background=BG_COLOR)
        style.configure("Main.TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_NORMAL)
        style.configure("TButton", font=FONT_BOLD, padding=5, background=BUTTON_COLOR, foreground=TEXT_COLOR, borderwidth=0)
        style.map("TButton", background=[('active', ACTIVE_BUTTON_COLOR)]) # Makes buttons change color on click.
        style.configure("Treeview", font=FONT_NORMAL, rowheight=25, fieldbackground=BG_COLOR, background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("Treeview.Heading", font=FONT_BOLD, background=BUTTON_COLOR, foreground=TEXT_COLOR)
        style.map("Treeview.Heading", background=[('active', ACTIVE_BUTTON_COLOR)])
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_BOLD, padding=[10, 5], background=BUTTON_COLOR, foreground=TEXT_COLOR)
        style.map("TNotebook.Tab", background=[("selected", ACTIVE_BUTTON_COLOR)])
        style.configure("TLabelframe", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_BOLD)
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_BOLD)
        style.configure("TEntry", fieldbackground=BUTTON_COLOR, foreground=TEXT_COLOR, borderwidth=0, insertcolor=TEXT_COLOR)

    def _create_main_menu_view(self):
        """Creates the main menu frame with navigation buttons."""
        self.main_menu_frame = ttk.Frame(self.main_container, style="Main.TFrame")

        # NOTE: To change the main title or add another icon,
        # you can modify this 'title_frame'.
        title_frame = ttk.Frame(self.main_menu_frame)
        title_frame.pack(pady=20)
        
        # Load and display the icon
        if PILLOW_AVAILABLE:
            try:
                # The path is relative to where main.py is run
                img = Image.open("assets/icon.png")
                img = img.resize((128, 100), Image.Resampling.LANCZOS)
                self.app_icon = ImageTk.PhotoImage(img)
                icon_label = ttk.Label(title_frame, image=self.app_icon)
                icon_label.pack(side='left', padx=10)
            except FileNotFoundError:
                # If the icon is missing, we just don't show it. This prevents a crash.
                pass

        title_label = ttk.Label(title_frame, text="St. Basil Pantry System", font=(FONT_FAMILY, 24, "bold"))
        title_label.pack(side='left')

        # NOTE: If you want to add a new main menu button, you can add it
        # here in the 'button_frame'.
        button_frame = ttk.Frame(self.main_menu_frame)
        button_frame.pack(fill='x', padx=50)
        dist_button = ttk.Button(button_frame, text="Manage Distributions", command=self.show_notebook_dist)
        dist_button.pack(side='left', fill='x', expand=True, ipady=15, padx=10)
        log_button = ttk.Button(button_frame, text="Log Donations", command=self.show_notebook_log)
        log_button.pack(side='left', fill='x', expand=True, ipady=15, padx=10)

        activity_frame = ttk.LabelFrame(self.main_menu_frame, text="Recent Activity")
        activity_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        cols = ('Time', 'Type', 'Details')
        self.activity_tree = ttk.Treeview(activity_frame, columns=cols, show='headings')
        for col in cols:
            self.activity_tree.heading(col, text=col)
        self.activity_tree.column("Time", width=120)
        self.activity_tree.column("Type", width=100)
        self.activity_tree.pack(expand=True, fill='both')
        
        status_frame = ttk.LabelFrame(self.main_menu_frame, text="Pantry Status")
        status_frame.pack(pady=10, padx=50, fill='x')
        
        self.households_waiting_label = ttk.Label(status_frame, text="Households Currently Waiting: 0")
        self.households_waiting_label.pack(anchor='w', padx=10, pady=5)
        
        self.inventory_items_label = ttk.Label(status_frame, text="Unique Items in Inventory: 0")
        self.inventory_items_label.pack(anchor='w', padx=10, pady=5)

    def _create_notebook_view(self):
        """Creates the tabbed notebook view but keeps it hidden initially."""
        self.notebook_frame = ttk.Frame(self.main_container)
        
        # We pack the back button first and set it to the bottom, so it's
        # always visible and doesn't get pushed off-screen if the window is resized.
        back_button = ttk.Button(self.notebook_frame, text="< Back to Main Menu", command=self.show_main_menu)
        back_button.pack(side='bottom', pady=10)

        self._create_menu() 
        self._create_notebook()
        self._create_food_donation_tab()
        self._create_money_donation_tab()
        self._create_household_queue_tab()
        self._create_distribution_tab()

    # Navigation Methods
    # These functions handle switching between the main menu and the tabbed view.

    def show_main_menu(self):
        """Hides the notebook and shows the main menu."""
        self.notebook_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill='both')
        self._refresh_status_view()
        self._refresh_activity_log_view()

    def show_notebook_dist(self):
        """Shows the notebook and navigates to the distribution queue."""
        self.main_menu_frame.pack_forget()
        self.notebook_frame.pack(expand=True, fill='both')
        self.notebook.select(self.queue_tab)
        self._refresh_household_queue_view()

    def show_notebook_log(self):
        """Shows the notebook and navigates to the donation logging tab."""
        self.main_menu_frame.pack_forget()
        self.notebook_frame.pack(expand=True, fill='both')
        self.notebook.select(self.food_tab)

    # UI Creation Methods
    def _create_menu(self):
        menubar = tk.Menu(self, bg=BG_COLOR, fg=TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR, activeforeground=TEXT_COLOR, borderwidth=0)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR, activeforeground=TEXT_COLOR, borderwidth=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save Data', command=self.pantry_manager._save_data)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR, activeforeground=TEXT_COLOR, borderwidth=0)
        menubar.add_cascade(label='View', menu=view_menu)
        view_menu.add_command(label='View Inventory', command=self._open_inventory_window)
        view_menu.add_command(label='View Distributions', command=self._open_distributions_window)

        data_menu = tk.Menu(menubar, tearoff=0, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=ACTIVE_BUTTON_COLOR, activeforeground=TEXT_COLOR, borderwidth=0)
        menubar.add_cascade(label='Data', menu=data_menu)
        data_menu.add_command(label='View Distribution Graph', command=self._open_graph_window)

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.notebook_frame)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        # Binding to this event allows us to run a function (like refreshing data)
        # automatically whenever the user clicks on a different tab.
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _create_food_donation_tab(self):
        self.food_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.food_tab, text='Food Donation')
        
        donor_frame = ttk.Frame(self.food_tab)
        donor_frame.pack(fill='x', padx=5, pady=5)
        self.food_donor_var = tk.StringVar()
        ttk.Label(donor_frame, text='Donor Name:').pack(side='left', padx=5)
        ttk.Entry(donor_frame, textvariable=self.food_donor_var).pack(side='left', fill='x', expand=True)

        add_item_frame = ttk.LabelFrame(self.food_tab, text="Add Item to Donation")
        add_item_frame.pack(fill='x', padx=5, pady=5)
        
        self.food_item_var = tk.StringVar()
        self.food_quantity_var = tk.StringVar()
        self.food_expiry_var = tk.StringVar()
        
        ttk.Label(add_item_frame, text='Item Name:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(add_item_frame, textvariable=self.food_item_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(add_item_frame, text='Quantity:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(add_item_frame, textvariable=self.food_quantity_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(add_item_frame, text='Expiration (YYYY-MM-DD):').grid(row=2, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(add_item_frame, textvariable=self.food_expiry_var).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(add_item_frame, text='Add Item', command=self._handle_add_item_to_donation).grid(row=3, column=1, sticky='e', padx=5, pady=5)

        donation_list_frame = ttk.LabelFrame(self.food_tab, text="Current Donation Items")
        donation_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        cols = ('Item', 'Quantity', 'Expires')
        self.donation_items_tree = ttk.Treeview(donation_list_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.donation_items_tree.heading(col, text=col)
        self.donation_items_tree.pack(side='left', fill='both', expand=True)
        
        donation_button_frame = ttk.Frame(donation_list_frame)
        donation_button_frame.pack(side='top', fill='x', padx=5)
        ttk.Button(donation_button_frame, text="Remove Selected", command=self._handle_remove_item_from_donation).pack(pady=5)
        ttk.Button(donation_button_frame, text="Clear All Items", command=self._handle_clear_donation).pack(pady=5)

        ttk.Button(self.food_tab, text='Log Entire Donation', command=self._handle_log_entire_donation).pack(pady=10)

    def _create_money_donation_tab(self):
        self.money_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.money_tab, text='Money Donation')
        self.money_donor_var = tk.StringVar()
        self.money_amount_var = tk.StringVar()
        ttk.Label(self.money_tab, text='Donor Name:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.money_tab, textvariable=self.money_donor_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.money_tab, text='Amount Donated: $').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.money_tab, textvariable=self.money_amount_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.money_tab, text='Add Money Donation', command=self._handle_add_money_donation).grid(row=2, column=0, columnspan=2, pady=10)

    def _create_household_queue_tab(self):
        self.queue_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.queue_tab, text='Household Queue')
        signin_frame = ttk.LabelFrame(self.queue_tab, text="Sign In New Household")
        signin_frame.pack(fill="x", padx=5, pady=5)
        self.household_name_var = tk.StringVar()
        self.household_size_var = tk.StringVar()
        ttk.Label(signin_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(signin_frame, textvariable=self.household_name_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(signin_frame, text="Size:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(signin_frame, textvariable=self.household_size_var).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(signin_frame, text="Sign In", command=self._handle_household_signin).grid(row=2, column=0, columnspan=2, pady=10)
        
        queue_frame = ttk.LabelFrame(self.queue_tab, text="Waiting List")
        queue_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        cols = ('#', 'Household Name', 'Family Size')
        self.queue_tree = ttk.Treeview(queue_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.queue_tree.heading(col, text=col)
        self.queue_tree.column("#", width=50)
        self.queue_tree.pack(side='left', expand=True, fill='both')

        queue_button_frame = ttk.Frame(queue_frame)
        queue_button_frame.pack(side='left', fill='y', padx=5)
        ttk.Button(queue_button_frame, text="Remove Selected", command=self._handle_remove_household).pack(pady=5)

    def _create_distribution_tab(self):
        self.distribution_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.distribution_tab, text='Record Distribution')
        main_frame = ttk.Frame(self.distribution_tab)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        inv_frame = ttk.LabelFrame(main_frame, text="Available Inventory")
        inv_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.inventory_search_var = tk.StringVar()
        self.inventory_search_var.trace_add("write", self._handle_inventory_search)
        search_entry = ttk.Entry(inv_frame, textvariable=self.inventory_search_var)
        search_entry.pack(fill='x', padx=2, pady=2)
        
        inv_cols = ('Item', 'Qty')
        self.inventory_tree = ttk.Treeview(inv_frame, columns=inv_cols, show='headings', selectmode='browse')
        self.inventory_tree.heading('Item', text='Item')
        self.inventory_tree.heading('Qty', text='Qty')
        self.inventory_tree.column("Qty", width=50)
        self.inventory_tree.pack(expand=True, fill='both')
        
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(side='left', fill='y', padx=5)
        ttk.Button(action_frame, text="Add to Cart ->", command=self._handle_add_to_cart).pack(pady=10)
        ttk.Button(action_frame, text="<- Remove from Cart", command=self._handle_remove_from_cart).pack(pady=10)
        ttk.Button(action_frame, text="Clear Cart", command=self._handle_clear_cart).pack(pady=10)
        
        cart_frame = ttk.LabelFrame(main_frame, text="Household Shopping Cart")
        cart_frame.pack(side='left', fill='both', expand=True, padx=5)
        cart_cols = ('Item', 'Qty')
        self.cart_tree = ttk.Treeview(cart_frame, columns=cart_cols, show='headings', selectmode='browse')
        self.cart_tree.heading('Item', text='Item')
        self.cart_tree.heading('Qty', text='Qty')
        self.cart_tree.column("Qty", width=50)
        self.cart_tree.pack(expand=True, fill='both')
        
        ttk.Button(self.distribution_tab, text='Record Distribution for Selected Household', command=self._handle_record_distribution).pack(pady=10)

    # Event Handlers
    # They are called when a user interacts with a widget (like clicking a button).

    def _on_tab_changed(self, event):
        try:
            selected_tab_index = self.notebook.index(self.notebook.select())
            if selected_tab_index == 3: 
                self._refresh_inventory_view()
        except tk.TclError:
            pass

    def _handle_add_item_to_donation(self):
        item = self.food_item_var.get()
        quantity_str = self.food_quantity_var.get()
        expiry = self.food_expiry_var.get()

        if not all([item, quantity_str, expiry]):
            messagebox.showerror("Input Error", "Item Name, Quantity, and Expiration are required.")
            return

        try:
            quantity = int(quantity_str)
            self.current_donation_items.append({'name': item, 'quantity': quantity, 'expiration_date': expiry})
            self.food_item_var.set("")
            self.food_quantity_var.set("")
            self.food_expiry_var.set("")
            self._refresh_donation_items_view()
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a whole number.")

    def _handle_remove_item_from_donation(self):
        selected_item = self.donation_items_tree.focus()
        if not selected_item:
            return
        
        selected_values = self.donation_items_tree.item(selected_item)['values']
        item_to_remove = {'name': str(selected_values[0]), 'quantity': int(selected_values[1]), 'expiration_date': str(selected_values[2])}

        for item in self.current_donation_items:
            if (item['name'] == item_to_remove['name'] and
                item['quantity'] == item_to_remove['quantity'] and
                item['expiration_date'] == item_to_remove['expiration_date']):
                self.current_donation_items.remove(item)
                break
        
        self._refresh_donation_items_view()

    def _handle_clear_donation(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all items from this donation?"):
            self.current_donation_items.clear()
            self._refresh_donation_items_view()

    def _handle_log_entire_donation(self):
        donor = self.food_donor_var.get()
        if not donor:
            messagebox.showerror("Input Error", "Donor Name is required.")
            return
        if not self.current_donation_items:
            messagebox.showerror("Input Error", "There are no items to donate.")
            return

        try:
            self.pantry_manager.add_food_donation(donor, self.current_donation_items)
            messagebox.showinfo("Success", f"Donation from {donor} has been logged.")
            
            self.current_donation_items.clear()
            self.food_donor_var.set("")
            self._refresh_donation_items_view()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def _handle_add_money_donation(self):
        donor = self.money_donor_var.get()
        amount_str = self.money_amount_var.get()
        if not all([donor, amount_str]):
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            amount = float(amount_str)
            self.pantry_manager.add_money_donation(donor, amount)
            messagebox.showinfo("Success", "Money donation has been logged.")
            self.money_donor_var.set("")
            self.money_amount_var.set("")
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            
    def _handle_household_signin(self):
        name = self.household_name_var.get()
        size_str = self.household_size_var.get()
        if not all([name, size_str]):
            messagebox.showerror("Input Error", "Name and Size are required.")
            return
        try:
            size = int(size_str)
            self.pantry_manager.sign_in_household(name, size)
            messagebox.showinfo("Success", f"Household '{name}' has been signed in.")
            self.household_name_var.set("")
            self.household_size_var.set("")
            self._refresh_household_queue_view()
        except ValueError:
            messagebox.showerror("Input Error", "Size must be a whole number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def _handle_remove_household(self):
        selected_item = self.queue_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a household to remove.")
            return
        
        household_id = self.queue_tree.item(selected_item)['values'][0]
        household_name = self.queue_tree.item(selected_item)['values'][1]

        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{household_name}' from the queue?"):
            try:
                self.pantry_manager.remove_household_from_queue(household_id)
                self._refresh_household_queue_view()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _handle_add_to_cart(self):
        selected_item = self.inventory_tree.focus()
        if not selected_item:
            return
        item_name = self.inventory_tree.item(selected_item)['values'][0]
        if item_name in self.current_distribution_cart:
            self.current_distribution_cart[item_name] += 1
        else:
            self.current_distribution_cart[item_name] = 1
        self._refresh_cart_view()

    def _handle_remove_from_cart(self):
        selected_item = self.cart_tree.focus()
        if not selected_item:
            return
        item_name = self.cart_tree.item(selected_item)['values'][0]
        if item_name in self.current_distribution_cart:
            self.current_distribution_cart[item_name] -= 1
            if self.current_distribution_cart[item_name] <= 0:
                del self.current_distribution_cart[item_name]
        self._refresh_cart_view()

    def _handle_clear_cart(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear this household's cart?"):
            self.current_distribution_cart.clear()
            self._refresh_cart_view()

    def _handle_record_distribution(self):
        selected_household_item = self.queue_tree.focus()
        if not selected_household_item:
            messagebox.showerror("Selection Error", "Please select a household from the queue first.")
            return
        if not self.current_distribution_cart:
            messagebox.showerror("Input Error", "The shopping cart is empty.")
            return
        household_id = self.queue_tree.item(selected_household_item)['values'][0]
        items_taken_data = []
        for name, quantity in self.current_distribution_cart.items():
            items_taken_data.append({'name': name, 'quantity': quantity})
        try:
            self.pantry_manager.record_distribution(household_id, items_taken_data)
            messagebox.showinfo("Success", "Distribution recorded successfully.")
            self.current_distribution_cart.clear()
            self._refresh_cart_view()
            self._refresh_household_queue_view()
            self._refresh_inventory_view()
        except ValueError as e:
            messagebox.showerror("Distribution Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _handle_inventory_search(self, *args):
        self._refresh_inventory_view()

    # UI Refresh Methods#
    # These functions are crucial for keeping the UI in sync with the data.
    # They are called after any action that changes the data.
    
    def _refresh_status_view(self):
        status = self.pantry_manager.get_pantry_status()
        self.households_waiting_label.config(text=f"Households Currently Waiting: {status['households_waiting']}")
        self.inventory_items_label.config(text=f"Unique Items in Inventory: {status['unique_items_in_inventory']}")

    def _refresh_household_queue_view(self):
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        queue_data = self.pantry_manager.get_queue()
        for household in queue_data:
            self.queue_tree.insert('', tk.END, values=(household.id, household.name, household.size))
            
    def _refresh_inventory_view(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        search_term = self.inventory_search_var.get().lower()
        inventory_data = self.pantry_manager.get_inventory()
        for item in inventory_data:
            if item.quantity > 0 and search_term in item.name.lower():
                self.inventory_tree.insert('', tk.END, values=(item.name, item.quantity))

    def _refresh_cart_view(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for name, quantity in self.current_distribution_cart.items():
            self.cart_tree.insert('', tk.END, values=(name, quantity))
            
    def _refresh_donation_items_view(self):
        for item in self.donation_items_tree.get_children():
            self.donation_items_tree.delete(item)
        for item in self.current_donation_items:
            self.donation_items_tree.insert('', tk.END, values=(item['name'], item['quantity'], item['expiration_date']))

    def _refresh_activity_log_view(self):
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        all_activity = []
        for donation in self.pantry_manager.donations_log:
            details = f"${donation.details:.2f}" if donation.type == 'Money' else f"{len(donation.details)} food items"
            all_activity.append({'date': donation.date, 'type': f"Donation ({donation.type})", 'details': f"from {donation.donor}: {details}"})
        for dist in self.pantry_manager.distributions_log:
            details = f"{len(dist['items'])} items to {dist['household_name']}"
            all_activity.append({'date': dist['date'], 'type': "Distribution", 'details': details})
        all_activity.sort(key=lambda x: x['date'], reverse=True)
        for activity in all_activity[:10]:
            self.activity_tree.insert('', tk.END, values=(activity['date'], activity['type'], activity['details']))

    def _open_inventory_window(self):
        inv_window = tk.Toplevel(self)
        inv_window.title('Current Inventory')
        inv_window.geometry("600x400")
        cols = ('Item', 'Quantity', 'Expiration Date')
        tree = ttk.Treeview(inv_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
        tree.pack(expand=True, fill='both')
        inventory_data = self.pantry_manager.get_inventory()
        for item in inventory_data:
            if item.quantity > 0:
                tree.insert('', tk.END, values=(item.name, item.quantity, item.expiration_date))

    def _open_distributions_window(self):
        dist_window = tk.Toplevel(self)
        dist_window.title('Item Distributions History')
        dist_window.geometry("600x400")
        cols = ('Household', 'Items', 'Date')
        tree = ttk.Treeview(dist_window, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
        tree.pack(expand=True, fill='both')
        distribution_data = self.pantry_manager.distributions_log
        for record in distribution_data:
            items_str = ", ".join([f"{item['quantity']}x {item['name']}" for item in record['items']])
            tree.insert('', tk.END, values=(record['household_name'], items_str, record['date']))

    def _open_graph_window(self):
        """Opens a window with a graph of the most distributed items."""
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Dependency Error", "Matplotlib is not installed.\nPlease run 'pip install matplotlib' to use this feature.")
            return

        graph_window = tk.Toplevel(self)
        graph_window.title("Top Distributed Items")
        graph_window.geometry("800x600")
        graph_window.configure(bg=BG_COLOR)

        data = self.pantry_manager.get_analytics_data()

        if not data:
            ttk.Label(graph_window, text="No distribution data available to generate a graph.", font=FONT_BOLD).pack(pady=20)
            return

        # Prepare data for the plot
        items = list(data.keys())[:10] # Top 10 items
        quantities = list(data.values())[:10]
        items.reverse() # Reverse for horizontal bar chart
        quantities.reverse()

        # Create the plot
        fig = Figure(figsize=(8, 6), dpi=100, facecolor=BG_COLOR)
        ax = fig.add_subplot(111)

        ax.barh(items, quantities, color=ACTIVE_BUTTON_COLOR)
        
        # Style the plot to match our theme
        ax.set_facecolor(BG_COLOR)
        ax.tick_params(axis='x', colors=TEXT_COLOR)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        ax.spines['left'].set_color(TEXT_COLOR)
        ax.spines['bottom'].set_color(TEXT_COLOR)
        ax.spines['top'].set_color(BG_COLOR)
        ax.spines['right'].set_color(BG_COLOR)
        ax.set_xlabel('Total Quantity Distributed', color=TEXT_COLOR)
        ax.set_title('Most Popular Items', color=TEXT_COLOR, fontsize=16)
        
        fig.tight_layout()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')
