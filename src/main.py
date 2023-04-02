import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import Settings
from src.entities.guest import Guest
from src.repositories.guest.gsheets import GSheetGuestRepository
from src.repositories.guest.sqlite import SQLiteGuestRepository


class App:
    def __init__(self, settings: Settings):
        self.settings = settings
        match settings.REPOSITORY_TYPE:
            case "gsheets":
                self.guest_repository = GSheetGuestRepository(
                    settings=settings,
                    spreadsheet_id=settings.GUEST_SPREADSHEET_ID
                )
            case "sqlite":
                self.guest_repository = SQLiteGuestRepository(db_path=settings.SQLITE_DATABASE_PATH)
            case _:
                raise ValueError(f"Invalid repository type: {settings.REPOSITORY_TYPE}")
        self.app = FastAPI()
        self.__register_routes()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __register_routes(self):
        @self.app.get("/guests")
        def get_guests() -> list[Guest]:
            guests = self.guest_repository.list()
            return guests

        @self.app.post("/guests")
        def post_guest(guest: Guest) -> Guest:
            self.guest_repository.add(guest)
            return guest


if __name__ == "__main__":
    settings = Settings()
    app = App(settings=settings).app
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
