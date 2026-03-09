import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    pizza_name TEXT,
    quantity INTEGER,
    order_date TEXT,
    revenue REAL
)
""")

cursor.execute("""
INSERT INTO orders VALUES
(1,'Margherita',2,'2024-01-01',500),
(2,'Pepperoni',1,'2024-01-02',300),
(3,'Margherita',3,'2024-01-03',750),
(4,'Veggie Supreme',2,'2024-01-04',620),
(5,'Pepperoni',1,'2024-01-05',300),
(6,'Margherita',4,'2024-01-06',1000),
(7,'BBQ Chicken',2,'2024-01-07',700),
(8,'Farmhouse',3,'2024-01-08',900),
(9,'Pepperoni',2,'2024-01-09',600),
(10,'Veggie Supreme',1,'2024-01-10',310),
(11,'Margherita',2,'2024-01-11',500),
(12,'BBQ Chicken',3,'2024-01-12',1050),
(13,'Farmhouse',1,'2024-01-13',300),
(14,'Pepperoni',4,'2024-01-14',1200),
(15,'Margherita',1,'2024-01-15',250),
(16,'Veggie Supreme',3,'2024-01-16',930),
(17,'Farmhouse',2,'2024-01-17',600),
(18,'BBQ Chicken',1,'2024-01-18',350),
(19,'Pepperoni',2,'2024-01-19',600),
(20,'Margherita',5,'2024-01-20',1250)
""")

conn.commit()
conn.close()

print("Database created and populated successfully!")