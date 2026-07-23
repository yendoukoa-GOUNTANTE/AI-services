import sqlite3
import os
import secrets

db_path = 'project.db'

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure tables exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            api_key VARCHAR(120) UNIQUE NOT NULL,
            subscription_status VARCHAR(20) DEFAULT 'inactive',
            subscription_plan VARCHAR(20) DEFAULT 'free',
            stripe_customer_id VARCHAR(120),
            credits INTEGER DEFAULT 1000
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent (
            id INTEGER PRIMARY KEY,
            developer_id INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(500) NOT NULL,
            endpoint_url VARCHAR(200) NOT NULL,
            price_per_use INTEGER DEFAULT 50,
            category VARCHAR(50) DEFAULT 'General',
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(developer_id) REFERENCES user(id)
        )
    """)

    # Check if system user exists
    cursor.execute("SELECT id FROM user WHERE username = 'OfficialSystem'")
    user = cursor.fetchone()
    if not user:
        system_api_key = secrets.token_hex(16)
        cursor.execute("INSERT INTO user (username, api_key) VALUES ('OfficialSystem', ?)", (system_api_key,))
        user_id = cursor.lastrowid
        print(f"OfficialSystem user created with API Key: {system_api_key}")
    else:
        user_id = user[0]

    # Check if marketer agent exists
    cursor.execute("SELECT id FROM agent WHERE name = 'Elite Marketer Bot'")
    agent = cursor.fetchone()
    new_desc = 'Advanced marketing strategy, GTM configuration, and campaign management agent.'
    if not agent:
        cursor.execute("""
            INSERT INTO agent (developer_id, name, description, endpoint_url, price_per_use, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, 'Elite Marketer Bot', new_desc, 'http://localhost:5001/api/v1/marketing/assistance', 75, 'Business'))
        print("Marketer Agent registered")
    else:
        cursor.execute("""
            UPDATE agent SET description = ? WHERE name = 'Elite Marketer Bot'
        """, (new_desc,))
        print("Marketer Agent description updated")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
