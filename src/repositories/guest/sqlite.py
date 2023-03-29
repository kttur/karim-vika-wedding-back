from sqlite3 import connect

from src.entities.guest import Alcohol, Food, Guest, Presence, Transfer
from src.repositories.guest.base import BaseGuestRepository


class SQLiteGuestRepository(BaseGuestRepository):
    def __init__(self, db_path: str, table_name: str = 'guests'):
        self.db_path = db_path
        self.table_name = table_name
        with connect(self.db_path) as conn:
            conn.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                f'(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, '
                f'presence TEXT, food TEXT, alcohol TEXT, transfer TEXT)'
            )

    def add(self, guest: Guest) -> None:
        with connect(self.db_path) as conn:
            conn.execute(
                f'INSERT INTO {self.table_name} '
                f'(name, phone, presence, food, alcohol, transfer) VALUES (?, ?, ?, ?, ?, ?)',
                guest.to_list(),
            )

    def list(self) -> list[Guest]:
        with connect(self.db_path) as conn:
            records = conn.execute(f'SELECT * FROM {self.table_name}').fetchall()
        return [
            Guest(
                name=record[1],
                phone=record[2],
                presence=Presence.from_str(record[3]),
                food=Food.from_str(record[4]),
                alcohol=Alcohol.from_str(record[5]),
                transfer=Transfer.from_str(record[6]),
            )
            for record in records
        ]
