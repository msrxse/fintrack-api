import sys
import os
from datetime import date
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from app.database import SessionLocal
from app.models.user import User
from app.models.account import Account, AccountType
from app.models.category import Category, CategoryType
from app.models.transaction import Transaction, TransactionType
from app.models.budget import Budget, BudgetPeriod

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def seed():
    db = SessionLocal()

    try:
        if db.query(User).first():
            print("Database already seeded. Skipping.")
            return

        # ---- USERS ----
        users = [
            User(
                email="alice@example.com",
                full_name="Alice Martins",
                hashed_password=hash_password("password123"),
                is_active=True,
            ),
            User(
                email="bob@example.com",
                full_name="Bob Chen",
                hashed_password=hash_password("password123"),
                is_active=True,
            ),
            User(
                email="sara@example.com",
                full_name="Sara Okonkwo",
                hashed_password=hash_password("password123"),
                is_active=True,
            ),
        ]
        db.add_all(users)
        db.flush()

        alice, bob, sara = users

        # ---- ACCOUNTS ----
        accounts = [
            Account(user_id=alice.id, name="Main Checking", type=AccountType.checking, balance=Decimal("4250.00")),
            Account(user_id=alice.id, name="Savings", type=AccountType.savings, balance=Decimal("12000.00")),
            Account(user_id=alice.id, name="Visa Credit", type=AccountType.credit, balance=Decimal("-850.00")),

            Account(user_id=bob.id, name="Checking", type=AccountType.checking, balance=Decimal("1800.00")),
            Account(user_id=bob.id, name="Investment", type=AccountType.investment, balance=Decimal("34000.00")),

            Account(user_id=sara.id, name="Current Account", type=AccountType.checking, balance=Decimal("3100.00")),
            Account(user_id=sara.id, name="Emergency Fund", type=AccountType.savings, balance=Decimal("8500.00")),
        ]
        db.add_all(accounts)
        db.flush()

        alice_checking, alice_savings, alice_credit, bob_checking, bob_investment, sara_checking, sara_savings = accounts

        # ---- CATEGORIES (system-level) ----
        categories = [
            Category(name="Salary", type=CategoryType.income, is_system=True),
            Category(name="Freelance", type=CategoryType.income, is_system=True),
            Category(name="Investment Returns", type=CategoryType.income, is_system=True),
            Category(name="Rent", type=CategoryType.expense, is_system=True),
            Category(name="Groceries", type=CategoryType.expense, is_system=True),
            Category(name="Restaurants", type=CategoryType.expense, is_system=True),
            Category(name="Transport", type=CategoryType.expense, is_system=True),
            Category(name="Subscriptions", type=CategoryType.expense, is_system=True),
            Category(name="Healthcare", type=CategoryType.expense, is_system=True),
            Category(name="Shopping", type=CategoryType.expense, is_system=True),
            Category(name="Utilities", type=CategoryType.expense, is_system=True),
            Category(name="Travel", type=CategoryType.expense, is_system=True),
            Category(name="Entertainment", type=CategoryType.expense, is_system=True),
        ]
        db.add_all(categories)
        db.flush()

        cat = {c.name: c for c in categories}

        # ---- TRANSACTIONS ----
        transactions = [
            # Alice — Jan 2025
            Transaction(account_id=alice_checking.id, category_id=cat["Salary"].id, amount=Decimal("5200.00"), type=TransactionType.income, description="Monthly salary", merchant="Acme Corp", date=date(2025, 1, 1)),
            Transaction(account_id=alice_checking.id, category_id=cat["Rent"].id, amount=Decimal("1500.00"), type=TransactionType.expense, description="January rent", merchant="Landlord", date=date(2025, 1, 2)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("94.50"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 1, 5)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("15.99"), type=TransactionType.expense, description="Streaming", merchant="Netflix", date=date(2025, 1, 6)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("9.99"), type=TransactionType.expense, description="Music", merchant="Spotify", date=date(2025, 1, 6)),
            Transaction(account_id=alice_checking.id, category_id=cat["Transport"].id, amount=Decimal("32.00"), type=TransactionType.expense, description="Ride to airport", merchant="Uber", date=date(2025, 1, 8)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("67.20"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 1, 12)),
            Transaction(account_id=alice_credit.id, category_id=cat["Restaurants"].id, amount=Decimal("48.00"), type=TransactionType.expense, description="Dinner", merchant="Nobu", date=date(2025, 1, 14)),
            Transaction(account_id=alice_checking.id, category_id=cat["Utilities"].id, amount=Decimal("85.00"), type=TransactionType.expense, description="Electric bill", merchant="ConEd", date=date(2025, 1, 15)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("110.30"), type=TransactionType.expense, description="Big weekly shop", merchant="Trader Joe's", date=date(2025, 1, 19)),
            Transaction(account_id=alice_credit.id, category_id=cat["Shopping"].id, amount=Decimal("129.99"), type=TransactionType.expense, description="Winter jacket", merchant="Zara", date=date(2025, 1, 21)),
            Transaction(account_id=alice_checking.id, category_id=cat["Transport"].id, amount=Decimal("127.00"), type=TransactionType.expense, description="Monthly metro pass", merchant="MTA", date=date(2025, 1, 25)),
            Transaction(account_id=alice_checking.id, category_id=cat["Freelance"].id, amount=Decimal("800.00"), type=TransactionType.income, description="Design project", merchant="Client A", date=date(2025, 1, 28)),

            # Alice — Feb 2025
            Transaction(account_id=alice_checking.id, category_id=cat["Salary"].id, amount=Decimal("5200.00"), type=TransactionType.income, description="Monthly salary", merchant="Acme Corp", date=date(2025, 2, 1)),
            Transaction(account_id=alice_checking.id, category_id=cat["Rent"].id, amount=Decimal("1500.00"), type=TransactionType.expense, description="February rent", merchant="Landlord", date=date(2025, 2, 2)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("15.99"), type=TransactionType.expense, description="Streaming", merchant="Netflix", date=date(2025, 2, 6)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("9.99"), type=TransactionType.expense, description="Music", merchant="Spotify", date=date(2025, 2, 6)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("88.40"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 2, 8)),
            Transaction(account_id=alice_credit.id, category_id=cat["Restaurants"].id, amount=Decimal("62.50"), type=TransactionType.expense, description="Valentine's dinner", merchant="Le Bernardin", date=date(2025, 2, 14)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("73.10"), type=TransactionType.expense, description="Weekly shop", merchant="Trader Joe's", date=date(2025, 2, 15)),
            Transaction(account_id=alice_checking.id, category_id=cat["Healthcare"].id, amount=Decimal("25.00"), type=TransactionType.expense, description="GP visit copay", merchant="CityMD", date=date(2025, 2, 18)),
            Transaction(account_id=alice_checking.id, category_id=cat["Utilities"].id, amount=Decimal("78.00"), type=TransactionType.expense, description="Electric bill", merchant="ConEd", date=date(2025, 2, 20)),
            Transaction(account_id=alice_credit.id, category_id=cat["Shopping"].id, amount=Decimal("245.00"), type=TransactionType.expense, description="Laptop stand + keyboard", merchant="Amazon", date=date(2025, 2, 22)),
            Transaction(account_id=alice_checking.id, category_id=cat["Transport"].id, amount=Decimal("127.00"), type=TransactionType.expense, description="Monthly metro pass", merchant="MTA", date=date(2025, 2, 25)),

            # Alice — Mar 2025
            Transaction(account_id=alice_checking.id, category_id=cat["Salary"].id, amount=Decimal("5200.00"), type=TransactionType.income, description="Monthly salary", merchant="Acme Corp", date=date(2025, 3, 1)),
            Transaction(account_id=alice_checking.id, category_id=cat["Rent"].id, amount=Decimal("1500.00"), type=TransactionType.expense, description="March rent", merchant="Landlord", date=date(2025, 3, 2)),
            Transaction(account_id=alice_credit.id, category_id=cat["Travel"].id, amount=Decimal("420.00"), type=TransactionType.expense, description="Flight to Lisbon", merchant="TAP Air Portugal", date=date(2025, 3, 5)),
            Transaction(account_id=alice_credit.id, category_id=cat["Travel"].id, amount=Decimal("680.00"), type=TransactionType.expense, description="Hotel 4 nights", merchant="Booking.com", date=date(2025, 3, 5)),
            Transaction(account_id=alice_checking.id, category_id=cat["Groceries"].id, amount=Decimal("92.80"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 3, 16)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("15.99"), type=TransactionType.expense, description="Streaming", merchant="Netflix", date=date(2025, 3, 6)),
            Transaction(account_id=alice_credit.id, category_id=cat["Subscriptions"].id, amount=Decimal("9.99"), type=TransactionType.expense, description="Music", merchant="Spotify", date=date(2025, 3, 6)),
            Transaction(account_id=alice_checking.id, category_id=cat["Freelance"].id, amount=Decimal("1200.00"), type=TransactionType.income, description="Brand redesign", merchant="Client B", date=date(2025, 3, 20)),
            Transaction(account_id=alice_checking.id, category_id=cat["Utilities"].id, amount=Decimal("72.00"), type=TransactionType.expense, description="Electric bill", merchant="ConEd", date=date(2025, 3, 20)),
            Transaction(account_id=alice_checking.id, category_id=cat["Transport"].id, amount=Decimal("127.00"), type=TransactionType.expense, description="Monthly metro pass", merchant="MTA", date=date(2025, 3, 25)),

            # Bob — Jan 2025
            Transaction(account_id=bob_checking.id, category_id=cat["Salary"].id, amount=Decimal("7500.00"), type=TransactionType.income, description="Monthly salary", merchant="TechCorp", date=date(2025, 1, 1)),
            Transaction(account_id=bob_checking.id, category_id=cat["Rent"].id, amount=Decimal("2200.00"), type=TransactionType.expense, description="January rent", merchant="Landlord", date=date(2025, 1, 3)),
            Transaction(account_id=bob_checking.id, category_id=cat["Groceries"].id, amount=Decimal("210.00"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 1, 5)),
            Transaction(account_id=bob_checking.id, category_id=cat["Restaurants"].id, amount=Decimal("85.00"), type=TransactionType.expense, description="Dinner with friends", merchant="Nobu", date=date(2025, 1, 7)),
            Transaction(account_id=bob_checking.id, category_id=cat["Subscriptions"].id, amount=Decimal("15.99"), type=TransactionType.expense, description="Streaming", merchant="Netflix", date=date(2025, 1, 8)),
            Transaction(account_id=bob_checking.id, category_id=cat["Subscriptions"].id, amount=Decimal("14.99"), type=TransactionType.expense, description="Cloud storage", merchant="Dropbox", date=date(2025, 1, 8)),
            Transaction(account_id=bob_checking.id, category_id=cat["Shopping"].id, amount=Decimal("349.00"), type=TransactionType.expense, description="Headphones", merchant="Apple", date=date(2025, 1, 10)),
            Transaction(account_id=bob_checking.id, category_id=cat["Transport"].id, amount=Decimal("65.00"), type=TransactionType.expense, description="Rides", merchant="Uber", date=date(2025, 1, 15)),
            Transaction(account_id=bob_checking.id, category_id=cat["Entertainment"].id, amount=Decimal("120.00"), type=TransactionType.expense, description="Concert tickets", merchant="Ticketmaster", date=date(2025, 1, 18)),
            Transaction(account_id=bob_investment.id, category_id=cat["Investment Returns"].id, amount=Decimal("430.00"), type=TransactionType.income, description="Dividend payout", merchant="Vanguard", date=date(2025, 1, 20)),
            Transaction(account_id=bob_checking.id, category_id=cat["Groceries"].id, amount=Decimal("185.00"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 1, 22)),
            Transaction(account_id=bob_checking.id, category_id=cat["Utilities"].id, amount=Decimal("110.00"), type=TransactionType.expense, description="Utilities", merchant="ConEd", date=date(2025, 1, 25)),

            # Bob — Feb 2025
            Transaction(account_id=bob_checking.id, category_id=cat["Salary"].id, amount=Decimal("7500.00"), type=TransactionType.income, description="Monthly salary", merchant="TechCorp", date=date(2025, 2, 1)),
            Transaction(account_id=bob_checking.id, category_id=cat["Rent"].id, amount=Decimal("2200.00"), type=TransactionType.expense, description="February rent", merchant="Landlord", date=date(2025, 2, 3)),
            Transaction(account_id=bob_checking.id, category_id=cat["Shopping"].id, amount=Decimal("899.00"), type=TransactionType.expense, description="iPhone case + accessories", merchant="Apple", date=date(2025, 2, 5)),
            Transaction(account_id=bob_checking.id, category_id=cat["Restaurants"].id, amount=Decimal("145.00"), type=TransactionType.expense, description="Valentine's dinner", merchant="Per Se", date=date(2025, 2, 14)),
            Transaction(account_id=bob_checking.id, category_id=cat["Groceries"].id, amount=Decimal("195.00"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 2, 16)),
            Transaction(account_id=bob_checking.id, category_id=cat["Entertainment"].id, amount=Decimal("75.00"), type=TransactionType.expense, description="Sports event", merchant="StubHub", date=date(2025, 2, 20)),
            Transaction(account_id=bob_investment.id, category_id=cat["Investment Returns"].id, amount=Decimal("390.00"), type=TransactionType.income, description="Dividend payout", merchant="Vanguard", date=date(2025, 2, 20)),

            # Bob — Mar 2025
            Transaction(account_id=bob_checking.id, category_id=cat["Salary"].id, amount=Decimal("7500.00"), type=TransactionType.income, description="Monthly salary", merchant="TechCorp", date=date(2025, 3, 1)),
            Transaction(account_id=bob_checking.id, category_id=cat["Rent"].id, amount=Decimal("2200.00"), type=TransactionType.expense, description="March rent", merchant="Landlord", date=date(2025, 3, 3)),
            Transaction(account_id=bob_checking.id, category_id=cat["Travel"].id, amount=Decimal("1200.00"), type=TransactionType.expense, description="Weekend in Miami", merchant="Marriott", date=date(2025, 3, 7)),
            Transaction(account_id=bob_checking.id, category_id=cat["Travel"].id, amount=Decimal("380.00"), type=TransactionType.expense, description="Flights", merchant="Delta", date=date(2025, 3, 7)),
            Transaction(account_id=bob_checking.id, category_id=cat["Groceries"].id, amount=Decimal("220.00"), type=TransactionType.expense, description="Weekly shop", merchant="Whole Foods", date=date(2025, 3, 16)),
            Transaction(account_id=bob_checking.id, category_id=cat["Restaurants"].id, amount=Decimal("95.00"), type=TransactionType.expense, description="Team lunch", merchant="Nobu", date=date(2025, 3, 20)),
            Transaction(account_id=bob_investment.id, category_id=cat["Investment Returns"].id, amount=Decimal("510.00"), type=TransactionType.income, description="Dividend payout", merchant="Vanguard", date=date(2025, 3, 20)),

            # Sara — Jan 2025
            Transaction(account_id=sara_checking.id, category_id=cat["Salary"].id, amount=Decimal("4800.00"), type=TransactionType.income, description="Monthly salary", merchant="HealthPlus", date=date(2025, 1, 1)),
            Transaction(account_id=sara_checking.id, category_id=cat["Rent"].id, amount=Decimal("1200.00"), type=TransactionType.expense, description="January rent", merchant="Landlord", date=date(2025, 1, 2)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("78.60"), type=TransactionType.expense, description="Weekly shop", merchant="Aldi", date=date(2025, 1, 4)),
            Transaction(account_id=sara_checking.id, category_id=cat["Transport"].id, amount=Decimal("45.00"), type=TransactionType.expense, description="Bus pass", merchant="TfL", date=date(2025, 1, 5)),
            Transaction(account_id=sara_checking.id, category_id=cat["Subscriptions"].id, amount=Decimal("9.99"), type=TransactionType.expense, description="Music", merchant="Spotify", date=date(2025, 1, 6)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("65.40"), type=TransactionType.expense, description="Weekly shop", merchant="Lidl", date=date(2025, 1, 11)),
            Transaction(account_id=sara_checking.id, category_id=cat["Healthcare"].id, amount=Decimal("35.00"), type=TransactionType.expense, description="Prescription", merchant="Pharmacy", date=date(2025, 1, 13)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("82.10"), type=TransactionType.expense, description="Weekly shop", merchant="Aldi", date=date(2025, 1, 18)),
            Transaction(account_id=sara_checking.id, category_id=cat["Utilities"].id, amount=Decimal("65.00"), type=TransactionType.expense, description="Electric bill", merchant="British Gas", date=date(2025, 1, 20)),
            Transaction(account_id=sara_savings.id, category_id=cat["Freelance"].id, amount=Decimal("500.00"), type=TransactionType.income, description="Tutoring sessions", merchant="Private clients", date=date(2025, 1, 25)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("71.30"), type=TransactionType.expense, description="Weekly shop", merchant="Lidl", date=date(2025, 1, 25)),

            # Sara — Feb 2025
            Transaction(account_id=sara_checking.id, category_id=cat["Salary"].id, amount=Decimal("4800.00"), type=TransactionType.income, description="Monthly salary", merchant="HealthPlus", date=date(2025, 2, 1)),
            Transaction(account_id=sara_checking.id, category_id=cat["Rent"].id, amount=Decimal("1200.00"), type=TransactionType.expense, description="February rent", merchant="Landlord", date=date(2025, 2, 2)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("69.90"), type=TransactionType.expense, description="Weekly shop", merchant="Aldi", date=date(2025, 2, 8)),
            Transaction(account_id=sara_checking.id, category_id=cat["Transport"].id, amount=Decimal("45.00"), type=TransactionType.expense, description="Bus pass", merchant="TfL", date=date(2025, 2, 5)),
            Transaction(account_id=sara_checking.id, category_id=cat["Restaurants"].id, amount=Decimal("38.00"), type=TransactionType.expense, description="Lunch out", merchant="Pret a Manger", date=date(2025, 2, 12)),
            Transaction(account_id=sara_checking.id, category_id=cat["Healthcare"].id, amount=Decimal("55.00"), type=TransactionType.expense, description="Dental checkup", merchant="Dental clinic", date=date(2025, 2, 15)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("74.20"), type=TransactionType.expense, description="Weekly shop", merchant="Lidl", date=date(2025, 2, 22)),
            Transaction(account_id=sara_savings.id, category_id=cat["Freelance"].id, amount=Decimal("500.00"), type=TransactionType.income, description="Tutoring sessions", merchant="Private clients", date=date(2025, 2, 25)),

            # Sara — Mar 2025
            Transaction(account_id=sara_checking.id, category_id=cat["Salary"].id, amount=Decimal("4800.00"), type=TransactionType.income, description="Monthly salary", merchant="HealthPlus", date=date(2025, 3, 1)),
            Transaction(account_id=sara_checking.id, category_id=cat["Rent"].id, amount=Decimal("1200.00"), type=TransactionType.expense, description="March rent", merchant="Landlord", date=date(2025, 3, 2)),
            Transaction(account_id=sara_checking.id, category_id=cat["Transport"].id, amount=Decimal("45.00"), type=TransactionType.expense, description="Bus pass", merchant="TfL", date=date(2025, 3, 5)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("80.50"), type=TransactionType.expense, description="Weekly shop", merchant="Aldi", date=date(2025, 3, 8)),
            Transaction(account_id=sara_checking.id, category_id=cat["Shopping"].id, amount=Decimal("59.99"), type=TransactionType.expense, description="Books", merchant="Amazon", date=date(2025, 3, 10)),
            Transaction(account_id=sara_checking.id, category_id=cat["Groceries"].id, amount=Decimal("66.70"), type=TransactionType.expense, description="Weekly shop", merchant="Lidl", date=date(2025, 3, 15)),
            Transaction(account_id=sara_checking.id, category_id=cat["Utilities"].id, amount=Decimal("60.00"), type=TransactionType.expense, description="Electric bill", merchant="British Gas", date=date(2025, 3, 20)),
            Transaction(account_id=sara_savings.id, category_id=cat["Freelance"].id, amount=Decimal("650.00"), type=TransactionType.income, description="Tutoring sessions", merchant="Private clients", date=date(2025, 3, 25)),
        ]
        db.add_all(transactions)

        # ---- BUDGETS ----
        budgets = [
            Budget(user_id=alice.id, category_id=cat["Groceries"].id, limit_amount=Decimal("400.00"), period=BudgetPeriod.monthly),
            Budget(user_id=alice.id, category_id=cat["Restaurants"].id, limit_amount=Decimal("200.00"), period=BudgetPeriod.monthly),
            Budget(user_id=alice.id, category_id=cat["Shopping"].id, limit_amount=Decimal("300.00"), period=BudgetPeriod.monthly),
            Budget(user_id=alice.id, category_id=cat["Transport"].id, limit_amount=Decimal("200.00"), period=BudgetPeriod.monthly),

            Budget(user_id=bob.id, category_id=cat["Groceries"].id, limit_amount=Decimal("600.00"), period=BudgetPeriod.monthly),
            Budget(user_id=bob.id, category_id=cat["Restaurants"].id, limit_amount=Decimal("400.00"), period=BudgetPeriod.monthly),
            Budget(user_id=bob.id, category_id=cat["Entertainment"].id, limit_amount=Decimal("200.00"), period=BudgetPeriod.monthly),

            Budget(user_id=sara.id, category_id=cat["Groceries"].id, limit_amount=Decimal("300.00"), period=BudgetPeriod.monthly),
            Budget(user_id=sara.id, category_id=cat["Transport"].id, limit_amount=Decimal("100.00"), period=BudgetPeriod.monthly),
            Budget(user_id=sara.id, category_id=cat["Healthcare"].id, limit_amount=Decimal("100.00"), period=BudgetPeriod.monthly),
        ]
        db.add_all(budgets)

        db.commit()
        print(f"Seeded: {len(users)} users, {len(accounts)} accounts, {len(categories)} categories, {len(transactions)} transactions, {len(budgets)} budgets.")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
