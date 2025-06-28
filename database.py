import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

class BudgetDatabase:
    def __init__(self, db_path="budget_coach.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create categories table with default categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                color TEXT DEFAULT '#1f77b4'
            )
        ''')
        
        # Create budget targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                monthly_target REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category) REFERENCES categories (name)
            )
        ''')
        
        # Create users table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                login_count INTEGER DEFAULT 1,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Add password_hash column if it doesn't exist (for existing databases)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN password_hash TEXT')
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
        # Create user sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_end TIMESTAMP,
                pages_visited INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default categories if they don't exist
        default_expense_categories = [
            ('Housing', 'expense', '#ff7f0e'),
            ('Transportation', 'expense', '#2ca02c'),
            ('Food & Dining', 'expense', '#d62728'),
            ('Entertainment', 'expense', '#9467bd'),
            ('Shopping', 'expense', '#8c564b'),
            ('Healthcare', 'expense', '#e377c2'),
            ('Education', 'expense', '#7f7f7f'),
            ('Utilities', 'expense', '#bcbd22'),
            ('Other', 'expense', '#17becf')
        ]
        
        default_income_categories = [
            ('Salary', 'income', '#2ca02c'),
            ('Freelance', 'income', '#1f77b4'),
            ('Investment', 'income', '#ff7f0e'),
            ('Other Income', 'income', '#9467bd')
        ]
        
        for category, cat_type, color in default_expense_categories + default_income_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, type, color) 
                VALUES (?, ?, ?)
            ''', (category, cat_type, color))
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, date, description, amount, category, transaction_type):
        """Add a new transaction to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (date, description, amount, category, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, description, amount, category, transaction_type))
        
        conn.commit()
        conn.close()
    
    def get_transactions(self, start_date=None, end_date=None):
        """Get transactions from the database"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM transactions"
        params = []
        
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params = [start_date, end_date]
        elif start_date:
            query += " WHERE date >= ?"
            params = [start_date]
        elif end_date:
            query += " WHERE date <= ?"
            params = [end_date]
        
        query += " ORDER BY date DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_categories(self, category_type=None):
        """Get categories from the database"""
        conn = sqlite3.connect(self.db_path)
        
        if category_type:
            df = pd.read_sql_query(
                "SELECT * FROM categories WHERE type = ? ORDER BY name", 
                conn, params=[category_type]
            )
        else:
            df = pd.read_sql_query("SELECT * FROM categories ORDER BY name", conn)
        
        conn.close()
        return df
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
    
    def export_to_csv(self, filepath):
        """Export all transactions to CSV"""
        df = self.get_transactions()
        df.to_csv(filepath, index=False)
        return len(df)
    
    def import_from_csv(self, filepath):
        """Import transactions from CSV"""
        df = pd.read_csv(filepath)
        conn = sqlite3.connect(self.db_path)
        
        # Validate required columns
        required_columns = ['date', 'description', 'amount', 'category', 'type']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        
        # Insert data
        df[required_columns].to_sql('transactions', conn, if_exists='append', index=False)
        conn.close()
        return len(df)
    
    def set_budget_target(self, category, monthly_target):
        """Set or update budget target for a category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if target already exists for this category
        cursor.execute("SELECT id FROM budget_targets WHERE category = ?", (category,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing target
            cursor.execute(
                "UPDATE budget_targets SET monthly_target = ? WHERE category = ?",
                (monthly_target, category)
            )
        else:
            # Insert new target
            cursor.execute(
                "INSERT INTO budget_targets (category, monthly_target) VALUES (?, ?)",
                (category, monthly_target)
            )
        
        conn.commit()
        conn.close()
    
    def get_budget_targets(self):
        """Get all budget targets"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM budget_targets ORDER BY category", conn)
        conn.close()
        return df
    
    def delete_budget_target(self, category):
        """Delete budget target for a category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM budget_targets WHERE category = ?", (category,))
        conn.commit()
        conn.close()
    
    def create_user(self, email, name=None):
        """Create a new user or return existing user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Update last login and login count
            cursor.execute('''
                UPDATE users 
                SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
                WHERE email = ?
            ''', (email,))
            user_id = existing_user[0]
        else:
            # Create new user
            cursor.execute('''
                INSERT INTO users (email, name, last_login) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (email, name))
            user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return user_id
    
    def get_user(self, email):
        """Get user by email (legacy method)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_user_by_email(self, email):
        """Get user by email with dictionary format"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, name, password_hash, created_at, last_login, login_count, is_active 
            FROM users WHERE email = ? AND is_active = 1
        """, (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'email': row[1],
                'name': row[2],
                'password_hash': row[3],
                'created_at': row[4],
                'last_login': row[5],
                'login_count': row[6],
                'is_active': row[7]
            }
        return None
    
    def create_user_with_password(self, email, name, password_hash):
        """Create a new user with password authentication"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (email, name, password_hash, last_login, login_count) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
            ''', (email, name, password_hash))
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            # User already exists
            conn.close()
            return None
    
    def update_user_login(self, user_id):
        """Update user login timestamp and count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP, login_count = login_count + 1 
            WHERE id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
    
    def start_user_session(self, user_id):
        """Start a new user session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_sessions (user_id) VALUES (?)
        ''', (user_id,))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def update_session_activity(self, session_id):
        """Update session with page visit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_sessions 
            SET pages_visited = pages_visited + 1 
            WHERE id = ?
        ''', (session_id,))
        conn.commit()
        conn.close()
    
    def get_user_stats(self):
        """Get user statistics for admin dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        # Total users
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Active users (logged in within last 30 days)
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE last_login >= datetime('now', '-30 days')
        ''')
        active_users = cursor.fetchone()[0]
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM user_sessions")
        total_sessions = cursor.fetchone()[0]
        
        conn.close()
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_sessions': total_sessions
        } 