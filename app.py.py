from flask import Flask, render_template_string, request
import sqlite3
import os

# ساخت پروژه Flask
app = Flask(__name__)

# مسیر دیتابیس SQLite
DB_PATH = "products.db"

# ساخت دیتابیس و جدول محصولات اگر وجود نداشته باشه
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """)
        # نمونه محصولات اولیه
        products = [
            ("روتختی نگین", 920),
            ("روتختی سوپر", 900),
            ("روتختی مدرن", 1200)
        ]
        c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", products)
        conn.commit()
        conn.close()

init_db()

# صفحه اصلی
@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, price FROM products")
    products = c.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>فروشگاه روتختی</title>
        <style>
            body { font-family: Tahoma; background: #f8f8f8; padding: 20px; }
            .product { border: 1px solid #ccc; padding: 10px; margin: 10px; background: white; display: inline-block; width: 200px; }
            .price { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>فروشگاه روتختی</h1>
        {% for id, name, price in products %}
            <div class="product">
                <h3>{{ name }}</h3>
                <p class="price">{{ price }} تومان</p>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, products=products)

# اجرای برنامه
if __name__ == "__main__":
    app.run(debug=True)
