from main import ProductApp
import os
import sqlite3

def test_addproduct(qtbot):
    test_db = "test_products.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,  
                category TEXT NOT NULL
            )
        """)
    conn.close()
    
    app = ProductApp() 
    app.db.conn = sqlite3.connect(test_db) 
    app.db.cursor = app.db.conn.cursor()
    qtbot.addWidget(app)
    
    app.db.add_product("asfasfasf", "12.0", "asofmsao")
    app.load_products()
    assert app.table.rowCount() == 1
    
    app.close()
    os.remove(test_db)