# supervisor.py

import sqlite3
from member_gym import Member, Gym  # Assuming member_gym.py is your main file

class Supervisor:
    def __init__(self, name, gym):
        self.name = name
        self.gym = gym

    def view_members(self):
        members = self.gym.get_members()
        for member in members:
            print(f"ID: {member.id}, Name: {member.name}, Membership Type: {member.membership_type}")

    def add_member(self, name, membership_type, fingerprint):
        fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()
        # Assuming IDs are auto-incremented and not duplicated.
        member_id = len(self.gym.members) + 1
        member = Member(member_id, name, membership_type, fingerprint_hash)
        self.gym.add_member(member)

    def remove_member(self, member_id):
        self.gym.cursor.execute('''
            DELETE FROM members WHERE id = ?
        ''', (member_id,))
        self.gym.connection.commit()

        self.gym.members = [member for member in self.gym.members if member.id != member_id]

    def edit_member(self, member_id, name=None, membership_type=None, fingerprint=None):
        if name or membership_type or fingerprint:
            member = next((member for member in self.gym.members if member.id == member_id), None)
            if member:
                if name:
                    member.name = name
                if membership_type:
                    member.membership_type = membership_type
                if fingerprint:
                    member.fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()

                self.gym.cursor.execute('''
                    UPDATE members SET name = ?, membership_type = ?, fingerprint_hash = ? WHERE id = ?
                ''', (member.name, member.membership_type, member.fingerprint_hash, member_id))
                self.gym.connection.commit()
