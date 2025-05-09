import sqlite3


def get_balance(account_number, owner):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT balance FROM accounts where id=? and owner=?''',
                    (account_number, owner))
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    finally:
        con.close()


def do_transfer(source, target, amount):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id FROM accounts where id=?''',
                    (target,))
        row = cur.fetchone()
        if row is None:
            return False
        cur.execute('''
            UPDATE accounts SET balance=balance-? where id=?''',
                    (amount, source))
        cur.execute('''
            UPDATE accounts SET balance=balance+? where id=?''',
                    (amount, target))
        con.commit()
        return True
    finally:
        con.close()


def get_accounts_for_email(email):
    conn = sqlite3.connect('bank.db')  # Assuming you're using SQLite
    cursor = conn.cursor()

    cursor.execute('''
            SELECT id, balance FROM accounts WHERE owner=?''',
                   (email,)
                   )

    accounts = [{'id': row[0], 'balance': row[1]} for row in cursor.fetchall()]

    conn.close()
    return accounts
