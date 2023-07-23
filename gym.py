# Very Extensive Modular Gym Attendance Management Software

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

# Checking in members
john_fingerprint_input = hashlib.sha256("John's Fingerprint".encode()).hexdigest()
gym.check_in_member(john_fingerprint_input)

sarah_fingerprint_input = hashlib.sha256("Sarah's Fingerprint".encode()).hexdigest()
gym.check_in_member(sarah_fingerprint_input)

unknown_fingerprint_input = hashlib.sha256("Unknown Fingerprint".encode()).hexdigest()
gym.check_in_member(unknown_fingerprint_input)

# Retrieving check-ins
john_check_ins = gym.get_check_ins(1)  # Assuming John's member_id is 1
print(f"John's check-ins: {john_check_ins}")

sarah_check_ins = gym.get_check_ins(2)  # Assuming Sarah's member_id is 2
print(f"Sarah's check-ins: {sarah_check_ins}")

# Supervisor viewing all members
supervisor.view_members()

# Supervisor removing a member
supervisor.remove_member(2)  # Assuming Sarah's member_id is 2

# Supervisor editing a member's information
supervisor.edit_member(1, name="Johnathon Doe")  # Assuming John's member_id is 1
# Usage example
gym = Gym("My Gym")

# Adding members
john_fingerprint = hashlib.sha256("John's Fingerprint".encode()).hexdigest()
john = Member("John Doe", "Premium", john_fingerprint)
gym.add_member(john)

sarah_fingerprint = hashlib.sha256("Sarah's Fingerprint".encode()).hexdigest()
sarah = Member("Sarah Smith", "Standard", sarah_fingerprint)
gym.add_member(sarah)

# Checking in members
john_fingerprint_input = hashlib.sha256("John's Fingerprint".encode()).hexdigest()
gym.check_in_member(john_fingerprint_input)

sarah_fingerprint_input = hashlib.sha256("Sarah's Fingerprint".encode()).hexdigest()
gym.check_in_member(sarah_fingerprint_input)

unknown_fingerprint_input = hashlib.sha256("Unknown Fingerprint".encode()).hexdigest()
gym.check_in_member(unknown_fingerprint_input)

# Retrieving check-ins
john_check_ins = gym.get_check_ins(1)  # Assuming John's member_id is 1
print(f"John's check-ins: {john_check_ins}")

sarah_check_ins = gym.get_check_ins(2)  # Assuming Sarah's member_id is 2
print(f"Sarah's check-ins: {sarah_check_ins}")
