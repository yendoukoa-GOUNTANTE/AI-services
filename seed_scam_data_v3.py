import sqlite3
import os
from datetime import datetime

def seed_scam_data():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'project.db'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_data (
            id INTEGER PRIMARY KEY,
            prompt TEXT NOT NULL,
            completion TEXT NOT NULL,
            category VARCHAR(50) DEFAULT 'General',
            is_public BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    scam_data = [
        ("Email from 'Dr. Bakare Tunde' regarding a $20M inheritance. Needs $5,000 for 'transfer fees'. Is this a scam?",
         "YES. This is a classic 419 Scam (Advance Fee Fraud). Deceptive patterns identified: 1. Unsolicited high-value inheritance. 2. Request for upfront payment for 'fees'. 3. Impersonation of a high-status individual. Action: Block sender and do not respond.",
         "Security", 1),
        ("WhatsApp message: 'Hello, I accidentally sent you my 6-digit verification code. Can you please send it back to me?'",
         "YES. This is a Social Engineering scam used to hijack your WhatsApp account. Deceptive patterns: 1. Sense of urgency. 2. Request for a security code. Action: Do NOT share the code. Delete the message and block the contact.",
         "Security", 1),
        ("Phone call transcript: 'This is the IRS calling. There is a warrant for your arrest due to unpaid taxes. You must pay $1,000 in Apple Gift Cards immediately to clear your record.'",
         "YES. This is a Government Impersonation scam. Deceptive patterns: 1. Use of fear and intimidation (threat of arrest). 2. Demand for payment via untraceable methods (Gift Cards). Action: Hang up. The IRS does not call to demand immediate payment or accept gift cards.",
         "Security", 1),
        ("Facebook message from a friend's profile: 'Hey! I found this way to double your money in 2 hours using this crypto platform. Just send $500 to this wallet...'",
         "YES. This is an Account Takeover / Investment Scam. Deceptive patterns: 1. 'Get rich quick' promise. 2. Impersonation of a trusted contact. Action: Contact your friend through another channel to verify. Most likely their account was compromised.",
         "Security", 1),
        ("Analyze this 'Global Grazer' behavior: User signs up, creates 50 low-quality posts with links to a external site, and immediately tries to withdraw 'referral bonuses'.",
         "HIGH RISK. This matches the 'Global Grazer' pattern (platform exploitation). Deceptive patterns: 1. Rapid, high-volume activity immediately after signup. 2. Low-quality content used as a vehicle for external links. 3. Exploitation of bonus/referral systems. Recommendation: Flag account for manual review and restrict withdrawal capabilities.",
         "Security", 1)
    ]

    try:
        cursor.executemany(
            "INSERT INTO training_data (prompt, completion, category, is_public) VALUES (?, ?, ?, ?)",
            scam_data
        )
        conn.commit()
        print("Scam detection training data seeded successfully.")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_scam_data()
