
import datetime
import hashlib
from member_gym import Member, Gym  # Assuming member_gym.py is your main file

class Customer:
    def __init__(self, member):
        self.member = member

    def check_in(self, gym):
        fingerprint_input = hashlib.sha256(self.member.fingerprint_hash.encode()).hexdigest()
        gym.check_in_member(fingerprint_input)

    def fill_details(self, name=None, membership_type=None, fingerprint=None):
        if name:
            self.member.name = name
        if membership_type:
            self.member.membership_type = membership_type
        if fingerprint:
            self.member.fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()
