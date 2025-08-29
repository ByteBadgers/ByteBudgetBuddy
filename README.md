# ByteBudgetBuddy

ByteBudgetBuddy is a personal finance tracker built with **Flask (Python)** and **SQLite**.  
It provides a web-based dashboard to track income, expenses, balances, and generate financial summaries.

---

## Features
- Add income and expense transactions
- Automatic summary report (Balance, Total Income, Total Expenses)
- Category breakdowns (e.g., Groceries, Rent, Entertainment)
- View all transactions in a structured table
- Export transactions to CSV
- Flash messages for user feedback with fade-away effect

---

## Technology Stack
- **Backend:** Python 3, Flask
- **Database:** SQLite
- **Frontend:** HTML, Jinja2, CSS
- **Version Control:** Git + GitHub

---

## Screenshots

### Dashboard
<img width="1913" height="912" alt="Screenshot 2025-08-27 215650" src="https://github.com/user-attachments/assets/40898bfd-9187-4ff2-89be-bdbeef79343f" />


### Add Transaction
<img width="1917" height="907" alt="Screenshot 2025-08-27 215750" src="https://github.com/user-attachments/assets/1296fa91-c1bb-4ef4-a5d8-0b40518e23e6" />


---

## Installation and Setup

Clone the repository and run locally:

```bash
# Clone the repository
git clone https://github.com/ByteBadgers/ByteBudgetBuddy.git
cd ByteBudgetBuddy

# (Optional) Create a virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
