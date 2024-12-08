import tkinter as tk
from tkinter import messagebox, ttk

class FinanceManager:
    def __init__(self):
        self.users = {}
        self.financial_records = {}
        self.current_user = None
    
    def get_records(self, username):
        """Retrieve records for a user."""
        return self.financial_records.get(username, [])

    def register_user(self, username, password):
        """Register a new user."""
        if username in self.users:
            return False  # Username already exists
        self.users[username] = password  # Save the new user's credentials
        self.financial_records[username] = []  # Initialize an empty record list for the user
        return True

    def authenticate_user(self, username, password):
        """Authenticate an existing user."""
        if username in self.users and self.users[username] == password:
            self.current_user = username
            return True
        return False

    def add_record(self, description, amount, category, record_type):
        """Add a financial record for the current user."""
        if not self.current_user:
            return False  # No user logged in
        record = {
            "description": description,
            "amount": amount,
            "category": category,
            "record_type": record_type,
        }
        self.financial_records[self.current_user].append(record)
        return True

    def delete_record(self, index):
        """Delete a financial record for the current user by index."""
        if not self.current_user:
            return False  # No user logged in
        try:
            del self.financial_records[self.current_user][index]
            return True
        except IndexError:
            return False

   
    def calculate_total_income(self, username):
        """Calculate total income for the given user."""
        if not username:
            return None  # No user provided
        records = self.financial_records.get(username, [])
        income = sum(r["amount"] for r in records if r["record_type"].lower() == "income")
        return income

    def calculate_savings(self, username):
        """Calculate savings for the given user."""
        if not username:
            return None  # No user provided
        records = self.financial_records.get(username, [])
        income = sum(r["amount"] for r in records if r["record_type"].lower() == "income")
        expense = sum(r["amount"] for r in records if r["record_type"].lower() == "expense")
        return income - expense


class FinanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Personal Finance Manager")
        self.master.geometry("800x600") 
        self.manager = FinanceManager()
        self.current_user = None

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        
        self.show_login_screen()

    def show_login_screen(self):
        """Display the login screen."""
        self.clear_frame()
        tk.Label(self.main_frame, text="Login", font=("Arial", 24)).pack(pady=20)
        
        tk.Label(self.main_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.main_frame, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(self.main_frame, text="Register", command=self.show_register_screen).pack()

    def show_register_screen(self):
        """Display the register screen."""
        self.clear_frame()
        tk.Label(self.main_frame, text="Register", font=("Arial", 24)).pack(pady=20)
        
        tk.Label(self.main_frame, text="Username:").pack()
        self.reg_username_entry = tk.Entry(self.main_frame)
        self.reg_username_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Password:").pack()
        self.reg_password_entry = tk.Entry(self.main_frame, show="*")
        self.reg_password_entry.pack(pady=5)
        
        tk.Button(self.main_frame, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Login", command=self.show_login_screen).pack()

    def show_dashboard(self):
        """Display the dashboard for the logged-in user."""
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Welcome, {self.current_user}!", font=("Arial", 24)).pack(pady=20)
    
        tk.Button(self.main_frame, text="Add Record", command=self.add_record_screen).pack(pady=5)
        tk.Button(self.main_frame, text="View Records", command=self.view_records_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Generate Report", command=self.generate_report_screen).pack(pady=5)
        tk.Button(self.main_frame, text="Calculate Savings", command=self.calculate_savings).pack(pady=5)
        tk.Button(self.main_frame, text="View Spending Distribution", command=self.view_spending_distribution).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout_user).pack(pady=10)

    def add_record_screen(self):
        """Screen to add financial records."""
        self.clear_frame()
        tk.Label(self.main_frame, text="Add Record", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.main_frame, text="Description:").pack()
        description_entry = tk.Entry(self.main_frame)
        description_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Amount:").pack()
        amount_entry = tk.Entry(self.main_frame)
        amount_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Category:").pack()
        category_entry = tk.Entry(self.main_frame)
        category_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Type (income/expense):").pack()
        record_type_entry = tk.Entry(self.main_frame)
        record_type_entry.pack(pady=5)

        def save_record():
            description = description_entry.get()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return
            category = category_entry.get()
            record_type = record_type_entry.get()
            self.manager.add_record(description, amount, category, record_type)
            messagebox.showinfo("Success", "Record added successfully!")
            self.show_dashboard()

        tk.Button(self.main_frame, text="Save Record", command=save_record).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Dashboard", command=self.show_dashboard).pack()

    def view_records_screen(self):
        """Display records for the current user."""
        self.clear_frame()
        tk.Label(self.main_frame, text="Your Records", font=("Arial", 24)).pack(pady=20)

        records = self.manager.get_records(self.current_user)
        if not records:
            tk.Label(self.main_frame, text="No records found.").pack(pady=10)
        else:
            columns = ("Description", "Amount", "Category", "Type")
            tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
            for idx, record in enumerate(records):
                tree.insert("", "end", iid=idx, values=(record["description"], record["amount"], record["category"], record["record_type"]))
            tree.pack(fill="both", expand=True, pady=10)

            def delete_record():
                selected_item = tree.selection()
                if selected_item:
                    record_index = int(selected_item[0])
                    self.manager.delete_record(record_index)
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "Record deleted successfully!")

            tk.Button(self.main_frame, text="Delete Record", command=delete_record).pack(pady=10)

        tk.Button(self.main_frame, text="Back to Dashboard", command=self.show_dashboard).pack()

    def clear_frame(self):
        """Clear the main frame for a new screen."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def login_user(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.manager.authenticate_user(username, password):
            self.current_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register_user(self):
        """Handle user registration."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        if self.manager.register_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def logout_user(self):
        """Logout the current user."""
        self.current_user = None
        self.manager.current_user = None
        self.show_login_screen()

    def calculate_total_income(self):
        """Calculate and display total income for the current user."""
        income = self.manager.calculate_total_income()
        if income is not None:
            messagebox.showinfo("Total Income", f"Your total income is: {income}")
        else:
            messagebox.showerror("Error", "Please log in to calculate total income.")

    def calculate_savings(self):
        """Calculate and display savings for the current user."""
        savings = self.manager.calculate_savings()
        if savings is not None:
            messagebox.showinfo("Savings", f"Your total savings are: {savings}")
        else:
            messagebox.showerror("Error", "Please log in to calculate savings.")

    def view_spending_distribution(self):
        """View spending distribution."""
        messagebox.showinfo("Info", "This feature will be implemented later.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
