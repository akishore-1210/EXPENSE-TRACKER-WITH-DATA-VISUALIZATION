import json
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# File to store the data
DATA_FILE = 'expenses.json'

def load_data():
    """Load the data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}, "current_user": None}

def save_data(data):
    """Save the data to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def currency_format(amount):
    """Format the amount into currency style."""
    return "${:,.2f}".format(amount)

def create_user(data):
    """Create a new user."""
    username = input("Enter a username: ")
    if username in data['users']:
        print("Username already exists.")
        return
    password = input("Enter a password: ")
    data['users'][username] = {
        "password": password,
        "income": 0,
        "expenses": [],
        "categories": {},
        "budget": 0,
        "monthly_expenses": {},
    }
    print("User created successfully!")

def login(data):
    """Login for existing users."""
    username = input("Enter username: ")
    if username not in data['users']:
        print("Username not found.")
        return None
    password = input("Enter password: ")
    if data['users'][username]['password'] == password:
        print(f"Welcome {username}!")
        return username
    else:
        print("Incorrect password.")
        return None

def add_income(data, current_user):
    """Add income."""
    amount = float(input("Enter income amount: "))
    data['users'][current_user]['income'] += amount
    print(f"Income of {currency_format(amount)} added.")

def add_expense(data, current_user):
    """Add expense."""
    amount = float(input("Enter expense amount: "))
    description = input("Enter expense description: ")
    category = input("Enter expense category: ")
    date = input("Enter expense date (yyyy-mm-dd): ")
    date = datetime.strptime(date, '%Y-%m-%d').date()

    # Add to expenses list and categories
    data['users'][current_user]['expenses'].append({
        "amount": amount, "description": description, "category": category, "date": str(date)
    })
    if category in data['users'][current_user]['categories']:
        data['users'][current_user]['categories'][category] += amount
    else:
        data['users'][current_user]['categories'][category] = amount
    
    print(f"Expense of {currency_format(amount)} added under {category}.")

def add_recurring_expense(data, current_user):
    """Add a recurring expense."""
    amount = float(input("Enter recurring expense amount: "))
    description = input("Enter expense description: ")
    category = input("Enter expense category: ")
    frequency = input("Is this expense recurring? (monthly/weekly): ").lower()
    
    # Add to recurring expenses list
    data['users'][current_user]['expenses'].append({
        "amount": amount, "description": description, "category": category, "frequency": frequency, "recurring": True
    })
    if category in data['users'][current_user]['categories']:
        data['users'][current_user]['categories'][category] += amount
    else:
        data['users'][current_user]['categories'][category] = amount
    
    print(f"Recurring expense of {currency_format(amount)} added under {category} with {frequency} frequency.")

def set_budget(data, current_user):
    """Set monthly budget."""
    budget = float(input("Enter your monthly budget: "))
    data['users'][current_user]['budget'] = budget
    print(f"Monthly budget set to {currency_format(budget)}.")

def view_balance(data, current_user):
    """View balance (income - expenses)."""
    total_expenses = sum(expense['amount'] for expense in data['users'][current_user]['expenses'])
    balance = data['users'][current_user]['income'] - total_expenses
    print(f"Current balance: {currency_format(balance)}")

def generate_report(data, current_user):
    """Generate a report of expenses."""
    print("\nExpense Report:")
    for category, amount in data['users'][current_user]['categories'].items():
        print(f"{category}: {currency_format(amount)}")
    print(f"\nTotal Income: {currency_format(data['users'][current_user]['income'])}")
    total_expenses = sum(expense['amount'] for expense in data['users'][current_user]['expenses'])
    print(f"Total Expenses: {currency_format(total_expenses)}")
    print(f"Balance: {currency_format(data['users'][current_user]['income'] - total_expenses)}\n")
    
    # Visualize expenses
    visualize_expenses(data, current_user)
    
    # Export the report to CSV
    export_report_to_csv(data, current_user)

def visualize_expenses(data, current_user):
    """Visualize expenses with a pie chart."""
    categories = list(data['users'][current_user]['categories'].keys())
    expenses = list(data['users'][current_user]['categories'].values())
    
    plt.figure(figsize=(7, 7))
    plt.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses Breakdown by Category")
    plt.show()

def export_report_to_csv(data, current_user):
    """Export expense report to a CSV file."""
    with open(f'{current_user}_expense_report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Amount'])
        
        # Write categories and their expenses
        for category, amount in data['users'][current_user]['categories'].items():
            writer.writerow([category, amount])
        
        total_expenses = sum(expense['amount'] for expense in data['users'][current_user]['expenses'])
        writer.writerow(['Total Expenses', total_expenses])
        writer.writerow(['Balance', data['users'][current_user]['income'] - total_expenses])
        
    print("Report exported to '{current_user}_expense_report.csv'.")

def main():
    """Main function to run the Expense Tracker."""
    data = load_data()

    while True:
        print("\nExpense Tracker")
        if data["current_user"]:
            print(f"Current User: {data['current_user']}")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. Add Recurring Expense")
            print("4. Set Monthly Budget")
            print("5. View Balance")
            print("6. Generate Report")
            print("7. Logout")
        else:
            print("1. Create New User")
            print("2. Login")
        
        choice = input("Enter your choice: ")
        
        if data["current_user"]:
            current_user = data["current_user"]
            if choice == '1':
                add_income(data, current_user)
            elif choice == '2':
                add_expense(data, current_user)
            elif choice == '3':
                add_recurring_expense(data, current_user)
            elif choice == '4':
                set_budget(data, current_user)
            elif choice == '5':
                view_balance(data, current_user)
            elif choice == '6':
                generate_report(data, current_user)
            elif choice == '7':
                data["current_user"] = None
                print("Logged out.")
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == '1':
                create_user(data)
            elif choice == '2':
                username = login(data)
                if username:
                    data["current_user"] = username
            else:
                print("Invalid choice. Please try again.")
        
        save_data(data)

# Run the program
if __name__ == '__main__':
    main()
