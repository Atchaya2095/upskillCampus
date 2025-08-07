import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# --- Database Setup ---
try:
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    """)
    conn.commit()
except Exception as e:
    messagebox.showerror("Database Error", str(e))

# --- Expense Tracker App ---
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Variables
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.note_var = tk.StringVar()

        # --- UI Layout ---
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        # Labels and Entry Fields
        tk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.category_var, width=30).grid(row=0, column=1)

        tk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.amount_var, width=30).grid(row=1, column=1)

        tk.Label(input_frame, text="Note:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(input_frame, textvariable=self.note_var, width=30).grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Expense", command=self.add_expense, bg="green", fg="white", width=15).pack(pady=5)
        tk.Button(root, text="View Expenses", command=self.view_expenses, bg="blue", fg="white", width=15).pack(pady=5)

        # Treeview Frame
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Date", "Category", "Amount", "Note"), show='headings', height=10)
        for col in ("Date", "Category", "Amount", "Note"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(side=tk.LEFT)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # --- Add Expense Function ---
    def add_expense(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        note = self.note_var.get().strip()
        date = datetime.now().strftime("%Y-%m-%d")

        if not category or not amount:
            messagebox.showwarning("Input Error", "Please enter both category and amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return

        try:
            cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                           (date, category, amount, note))
            conn.commit()
            self.category_var.set("")
            self.amount_var.set("")
            self.note_var.set("")
            messagebox.showinfo("Success", "Expense added successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # --- View Expenses Function ---
    def view_expenses(self):
        self.tree.delete(*self.tree.get_children())
        try:
            cursor.execute("SELECT date, category, amount, note FROM expenses ORDER BY id DESC")
            for row in cursor.fetchall():
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
