from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str = None

    @property
    def username_display(self):
        return self.username if self.username else "null username"