import sqlite3

def generate_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Sample data for users
    users = [
        ('john_doe', 'john@example.com', 'Example Corp', 'USA', '12345', 'password123'),
        ('jane_doe', 'jane@example.com', 'Example Inc', 'Canada', '54321', 'password456'),
        ('alice_smith', 'alice@example.com', 'Tech Solutions', 'UK', '67890', 'password789'),
        ('bob_jones', 'bob@example.com', 'Innovate Ltd', 'Australia', '09876', 'password012')
    ]

    # Sample data for products
    products = [
        ('Product A', 19.99),
        ('Product B', 29.99),
        ('Product C', 39.99),
        ('Product D', 49.99)
    ]

    # Insert data into users table
    c.executemany('''
        INSERT INTO users (username, email, company, country, postcode, password) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users)

    # Insert data into products table
    c.executemany('''
        INSERT INTO products (name, price) 
        VALUES (?, ?)
    ''', products)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate_data()