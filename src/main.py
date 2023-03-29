from fastapi import FastAPI

from src.config.settings import Settings
from src.entities.guest import Guest
from src.repositories.guest.gsheets import GSheetGuestRepository

app = FastAPI()
settings = Settings()


@app.get("/guests")
def get_guests():
    guest_repository = GSheetGuestRepository(settings=settings, spreadsheet_id=settings.GUEST_SPREADSHEET_ID)
    guests = guest_repository.list()
    return guests


@app.post("/guests")
def post_guest(guest: Guest):
    guest_repository = GSheetGuestRepository(settings=settings, spreadsheet_id=settings.GUEST_SPREADSHEET_ID)
    guest_repository.add(guest)
    return guest


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
