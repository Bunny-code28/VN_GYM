# Gym Attendance Management Software

import datetime
import hashlib
import sqlite3

class Member:
    def __init__(self, name, membership_type, fingerprint_hash):
        self.name = name
        self.membership_type = membership_type
        self.fingerprint_hash = fingerprint_hash
        self.check_ins = []

    def check_in(self):
        now = datetime.datetime.now()
        self.check_ins.append(now)

    def get_check_ins(self):
        return self.check_ins

    def verify_fingerprint(self, fingerprint_hash):
        return self.fingerprint_hash == fingerprint_hash

class Gym:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.connection = sqlite3.connect('attendance_database.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                membership_type TEXT,
                fingerprint_hash TEXT
            )
        ''')
        self.connection.commit()

    def add_member(self, member):
        self.members.append(member)
        self.cursor.execute('''
            INSERT INTO members (name, membership_type, fingerprint_hash)
            VALUES (?, ?, ?)
        ''', (member.name, member.membership_type, member.fingerprint_hash))
        self.connection.commit()

    def get_members(self):
        self.cursor.execute("SELECT * FROM members")
        rows = self.cursor.fetchall()
        members = []
        for row in rows:
            name, membership_type, fingerprint_hash = row[1], row[2], row[3]
            member = Member(name, membership_type, fingerprint_hash)
            members.append(member)
        return members

    def check_in_member(self, fingerprint_hash):
        for member in self.members:
            if member.verify_fingerprint(fingerprint_hash):
                member.check_in()
                self.cursor.execute('''
                    INSERT INTO check_ins (member_id, check_in_time)
                    VALUES (?, ?)
                ''', (member.id, datetime.datetime.now()))
                self.connection.commit()
                print(f"{member.name} checked in at {datetime.datetime.now()}")
                break
        else:
            print("Fingerprint not recognized.")

    def get_check_ins(self, member_id):
        self.cursor.execute('''
            SELECT * FROM check_ins WHERE member_id = ?
        ''', (member_id,))
        rows = self.cursor.fetchall()
        check_ins = []
        for row in rows:
            check_ins.append(row[2])
        return check_ins
        
# Usage example
gym = Gym("My Gym")

# Creating a supervisor
supervisor = Supervisor("Alex", gym)

# Adding members using supervisor
supervisor.add_member("John Doe", "Premium", "John's Fingerprint")
supervisor.add_member("Sarah Smith", "Standard", "Sarah's Fingerprint")

# Creating a customer
john_member = gym.get_members()[0]  # Assuming John's member_id is 1
john = Customer(john_member)

# Customer checking in
john.check_in(gym)

# Customer filling in details
john.fill_details(name="Johnny Doe")

# Retrieving check-ins
john_check_ins = gym.get_check_ins(1)  # Assuming John's member_id is 1
print(f"John's check-ins: {john_check_ins}")

# Supervisor viewing all members
supervisor.view_members()

# Supervisor removing a member
supervisor.remove_member(2)  # Assuming Sarah's member_id is 2

# Supervisor editing a member's information
supervisor.edit_member(1, name="Johnathon Doe")  # Assuming John's member_id is 1
