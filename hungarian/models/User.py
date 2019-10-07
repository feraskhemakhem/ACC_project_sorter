from typing import List, Tuple, Dict, NewType
from .Project import Project

Email = NewType("Email", str)


class User(object):
    def __init__(self, name: str, email: str, preferences: Dict[str, int], slack: str):
        self.name = name
        self.email = email
        self.preferences = preferences
        self.slack = slack

    def __str__(self):
        return str(
            {
                "name": self.name,
                "email": self.email,
                "preferences": self.preferences,
                "slack": self.slack,
            }
        )

    def __repr__(self):
        return str(self)

    def dictify(self):
        return {"name": self.name, "email": self.email, "slack": self.slack}

