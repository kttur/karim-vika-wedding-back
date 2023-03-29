import json
import os

import google.auth
import pygsheets
from google.oauth2 import service_account

from src.config.settings import Settings
from src.entities.guest import Alcohol, Food, Guest, Presence, Transfer
from src.repositories.guest.base import BaseGuestRepository


class GSheetGuestRepository(BaseGuestRepository):
    def __init__(self, settings: Settings, spreadsheet_id: str):
        self.settings = settings
        self.client = pygsheets.authorize(custom_credentials=self.__read_credentials())
        self.spreadsheet_id = spreadsheet_id
        self._sheet = self.client.open_by_key(self.spreadsheet_id).sheet1

    def __read_credentials(self) -> service_account.Credentials:
        scopes = (
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets',
        )

        if self.settings.GOOGLE_APPLICATION_CREDENTIALS:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(self.settings.GOOGLE_APPLICATION_CREDENTIALS, strict=False),
                scopes=scopes,
            )
        elif self.settings.GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH:
            credentials = service_account.Credentials.from_service_account_file(
                os.path.expanduser(self.settings.GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH),
                scopes=scopes,
            )
        else:
            credentials, _ = google.auth.default(scopes=scopes)

        return credentials

    def add(self, guest: Guest) -> None:
        self._sheet.append_table([guest.to_list()])

    def list(self) -> list[Guest]:
        records = self._sheet.get_all_records()
        return [
            Guest(
                name=record['Name'],
                phone=record['Phone'],
                presence=Presence.from_str(record['Presence']),
                food=Food.from_str(record['Food']),
                alcohol=Alcohol.from_str(record['Alcohol']),
                transfer=Transfer.from_str(record['Transfer']),
            )
            for record in records
        ]
