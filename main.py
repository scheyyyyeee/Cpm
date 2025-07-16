import sqlite3
import os
import time
import json
import random
from datetime import datetime

DB_NAME = "users.db"
ADMIN_PASS = "admin123"
VERSION = "v2.3.1"

# ANSI color codes for vibrant visuals
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m"
}

# ASCII art for the intro
INTRO_ART = f"""
{COLORS['CYAN']}========================================
       CPM HACK TOOL {VERSION} 
                    VIP 
========================================{COLORS['RESET']}
"""

# ========== DB SETUP ==========

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        key TEXT DEFAULT ''
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS key_requests (
        email TEXT PRIMARY KEY,
        approved_key TEXT DEFAULT '',
        FOREIGN KEY(email) REFERENCES users(email)
    )
    ''')
    conn.commit()
    conn.close()

# ========== USER FUNCTIONS ==========

def user_exists(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def register_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

def login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    result = cur.fetchone()
    conn.close()
    return result

def request_key(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO key_requests (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()

def check_approved_key(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT approved_key FROM key_requests WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def save_approved_key(email, key):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE key_requests SET approved_key=? WHERE email=?", (key, email))
    cur.execute("UPDATE users SET key=? WHERE email=?", (key, email))
    conn.commit()
    conn.close()

# ========== ADMIN TOOL ==========

def admin_approve():
    print(f"{COLORS['YELLOW']} Admin Control Panel {COLORS['RESET']}")
    pw = input("Enter admin password: ")
    if pw != ADMIN_PASS:
        print(f"{COLORS['RED']}Access Denied! Incorrect password.{COLORS['RESET']}")
        return
    print(f"{COLORS['GREEN']}Access Granted!{COLORS['RESET']}")
    loader("Initializing admin tools")
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT email FROM key_requests WHERE approved_key=''")
    requests = cur.fetchall()

    if not requests:
        print(f"{COLORS['YELLOW']} No pending key requests.{COLORS['RESET']}")
        return

    for r in requests:
        email = r[0]
        key = input(f"Enter key for {email}: ").strip()
        if key:
            save_approved_key(email, key)
            print(f"{COLORS['GREEN']} Key approved for {email}!{COLORS['RESET']}")

# ========== VISUAL EFFECTS ==========

def loader(message):
    print(f"{COLORS['CYAN']}{message}{COLORS['RESET']}", end="")
    for _ in range(5):
        time.sleep(random.uniform(0.2, 0.5))
        print(".", end="", flush=True)
    print(f"{COLORS['GREEN']} Done!{COLORS['RESET']}")

def progress_bar():
    print(f"{COLORS['BLUE']}Processing: [", end="", flush=True)
    for _ in range(10):
        time.sleep(random.uniform(0.1, 0.3))
        print("█", end="", flush=True)
    print(f"] 100%{COLORS['RESET']}")

# ========== MAIN MENU ==========

def menu():
    features = [
        "Increase Money 1.5K", "Increase Coins 4.5K", "King Rank 8K", "Change ID 4.5K",
        "Change Name 100", "Change Name (Rainbow) 100", "Number Plates 2K", "Account Delete FREE",
        "Account Register FREE", "Delete Friends 500", "Unlock Paid Cars 5K", "Unlock All Cars 6K",
        "Unlock All Car Sirens 3.5K", "Unlock W16 Engine 4K", "Unlock All Horns 3K", "Unlock Disable Damage 3K",
        "Unlock Unlimited Fuel 3K", "Unlock House 3 4K", "Unlock Smoke 4K", "Unlock Heels 4K",
        "Unlock Animations 2K", "Unlock Equipments M 3K", "Unlock Equipments F 3K", "Change Race Wins 1K",
        "Change Race Loses 1K", "Clone Account 7K", "Custom Car HP 2.5K", "Custom Angle 1.5K",
        "Custom Tire Burner 1.5K", "Custom Car Brake 2K", "Custom Car Mileage 2K", "Remove Rear Bumper 2.5K",
        "Remove Front Bumper 2.5K", "Change Gmail 2K", "Change Password 2K", "Custom Spoiler 10K",
        "Custom Body Kit 10K", "Unlock Premium Wheels 4.5K", "Unlock Toyota Crown 2K",
        "Unlock Clan Hat (M) 3K", "Remove Head Male 3K", "Remove Head Female 3K", "Unlock Clan Top 1 (M) 3K",
        "Unlock Clan Top 2 (M) 3K", "Unlock Clan Top 3 (M) 3K", "Unlock Clan Top 1 (F) 3K",
        "Unlock Clan Top 2 (F) 3K", "Unlock Mercedes CLS 4K", "Car Incline 1K", "Unlock Lambo (iOS ONLY) 5K"
    ]
    
    prompt_input = {1, 2, 4, 24, 25, 27, 28, 29, 30, 31, 34, 35, 36, 37}

    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(f"{COLORS['CYAN']}{INTRO_ART}{COLORS['RESET']}")
        print(f"{COLORS['YELLOW']}AVAILABLE HACKS: {COLORS['RESET']}")
        print(f"{COLORS['RED']}{{00}}: Exit{COLORS['RESET']}")
        for i, name in enumerate(features, start=1):
            print(f"{COLORS['GREEN']}{{{i:02d}}}: {name}{COLORS['RESET']}")
        
        choice = input(f"\n{COLORS['BLUE']}Select hack (0 to exit): {COLORS['RESET']}").strip()

        if choice in {"0", "00"}:
            print(f"{COLORS['RED']}Shutting down hack tool...{COLORS['RESET']}")
            loader("Exiting system")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(features):
            index = int(choice) - 1
            selected_feature = features[index]
            if int(choice) in prompt_input:
                value = input(f"{COLORS['YELLOW']}Enter value for {selected_feature}: {COLORS['RESET']}").strip()
                print(f"{COLORS['CYAN']} Applying {value} to {selected_feature}...{COLORS['RESET']}")
            loader(f"Activating {selected_feature}")
            progress_bar()
            print(f"{COLORS['GREEN']}{selected_feature} hacked successfully! Enjoy!{COLORS['RESET']}")
            print(f"{COLORS['CYAN']} *BEEP BOOP* System updated at {datetime.now().strftime('%H:%M:%S')}{COLORS['RESET']}")
        else:
            print(f"{COLORS['RED']}Invalid hack option. Try again!{COLORS['RESET']}")
        
        input(f"\n{COLORS['YELLOW']}Press Enter to continue...{COLORS['RESET']}")

# ========== MAIN ==========

def main():
    init_db()
    print(INTRO_ART)
    print(f"{COLORS['GREEN']}Welcome to CPM Hack Tool {VERSION} - Elite Edition{COLORS['RESET']}")
    loader("Initializing hack environment")

    while True:
        print(f"\n{COLORS['BLUE']}1. Register\n2. Login\n3. Admin Approval\n0. Exit{COLORS['RESET']}")
        opt = input(f"{COLORS['YELLOW']}Choose option: {COLORS['RESET']}").strip()

        if opt == "1":
            email = input(f"{COLORS['CYAN']}Enter email: {COLORS['RESET']}").strip()
            if '@' not in email:
                print(f"{COLORS['RED']}Email must contain '@'{COLORS['RESET']}")
                continue
            password = input(f"{COLORS['CYAN']}Enter password: {COLORS['RESET']}").strip()
            if user_exists(email):
                print(f"{COLORS['RED']}User already exists!{COLORS['RESET']}")
            else:
                register_user(email, password)
                loader("Registering user")
                print(f"{COLORS['GREEN']}Registered successfully! Welcome aboard!{COLORS['RESET']}")

        elif opt == "2":
            email = input(f"{COLORS['CYAN']}Email: {COLORS['RESET']}").strip()
            password = input(f"{COLORS['CYAN']}Password: {COLORS['RESET']}").strip()
            user = login(email, password)
            if user:
                loader("Verifying credentials")
                approved_key = check_approved_key(email)
                if approved_key:
                    print(f"{COLORS['GREEN']}Access granted! Your key: {approved_key}{COLORS['RESET']}")
                    menu()
                else:
                    request_key(email)
                    print(f"{COLORS['YELLOW']} Key requested. Awaiting admin approval...{COLORS['RESET']}")
            else:
                print(f"{COLORS['RED']}Login failed. Check credentials.{COLORS['RESET']}")

        elif opt == "3":
            admin_approve()

        elif opt == "0":
            print(f"{COLORS['RED']} Terminating CPM Hack Tool...{COLORS['RESET']}")
            loader("Shutting down")
            break

        else:
            print(f"{COLORS['RED']}Invalid option. Please try again.{COLORS['RESET']}")

# ========== START ==========

if __name__ == "__main__":
    main()