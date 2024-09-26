from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('budget.db')
    return conn

# Create tables if not exists
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            category TEXT,
            amount REAL,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB tables
create_tables()

# Route to add a new transaction
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    description = data['description']
    category = data['category']
    amount = data['amount']
    date = data['date']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (description, category, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (description, category, amount, date))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Transaction added successfully'}), 201

# Route to get all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    
    transactions_list = []
    for trans in transactions:
        transactions_list.append({
            'id': trans[0],
            'description': trans[1],
            'category': trans[2],
            'amount': trans[3],
            'date': trans[4]
        })
    
    return jsonify(transactions_list), 200

# Route to get income vs expenses chart data
@app.route('/api/summary', methods=['GET'])
def get_summary():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount) FROM transactions WHERE amount > 0
    ''')
    income = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT SUM(amount) FROM transactions WHERE amount < 0
    ''')
    expenses = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'income': income,
        'expenses': abs(expenses)
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    try:
        c.execute("DELETE FROM transactions WHERE id=?", (id,))
        conn.commit()
        return jsonify({"message": "Transaction deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400