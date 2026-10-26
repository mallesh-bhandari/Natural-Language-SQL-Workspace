import sqlite3

# Creates a local sqlite database file named northwind.db automatically
conn = sqlite3.connect("northwind.db")
cursor = conn.cursor()

# 1. Create business tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    category_id INTEGER,
    unit_price REAL,
    units_in_stock INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Clear old records if re-running script
DELETE FROM orders;
DELETE FROM products;
DELETE FROM categories;
DELETE FROM customers;

-- Insert business categories
INSERT INTO categories (category_name, description) VALUES
('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
('Confections', 'Desserts, candies, and sweet breads'),
('Dairy Products', 'Cheeses, butter, and milk products');

-- Insert products
INSERT INTO products (product_name, category_id, unit_price, units_in_stock) VALUES
('Chai', 1, 18.00, 39),
('Chang', 1, 19.00, 17),
('Aniseed Syrup', 2, 10.00, 13),
('Chef Anton''s Cajun Seasoning', 2, 22.00, 53),
('Queso Manchego', 3, 38.00, 86);

-- Insert customers
INSERT INTO customers (company_name, city, country) VALUES
('Alfreds Futterkiste', 'Berlin', 'Germany'),
('Ana Trujillo Emparedados', 'México D.F.', 'Mexico'),
('Antonio Moreno Taquería', 'México D.F.', 'Mexico'),
('Around the Horn', 'London', 'UK');

-- Insert transactions / orders
INSERT INTO orders (customer_id, product_id, quantity, order_date, total_amount) VALUES
(1, 1, 10, '2026-01-15', 180.00),
(1, 2, 5, '2026-02-10', 95.00),
(2, 3, 20, '2026-02-12', 200.00),
(3, 4, 15, '2026-03-01', 330.00),
(4, 5, 8, '2026-03-05', 304.00),
(2, 1, 12, '2026-03-10', 216.00);
""")

conn.commit()
conn.close()

print("Success: SQLite database 'northwind.db' generated and populated with sample data!")