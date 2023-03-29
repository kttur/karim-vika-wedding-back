from dataclasses import dataclass
from pydantic import BaseModel


class StrMixin:
    def __str__(self):
        return ", ".join([k for k, v in self.__dict__.items() if v])

    @classmethod
    def from_str(cls, s: str):
        return cls(**{k: True for k in s.split(", ")})


class Presence(StrMixin, BaseModel):
    ceremony: bool = False
    restaurant: bool = False


class Food(StrMixin, BaseModel):
    meat: bool = False
    fish: bool = False
    bird: bool = False
    vegetarian: bool = False


class Alcohol(StrMixin, BaseModel):
    rum: bool = False
    whiskey: bool = False
    vodka: bool = False
    champagne: bool = False
    wine: bool = False
    beer: bool = False
    non_alcoholic: bool = False


class Transfer(StrMixin, BaseModel):
    before: bool = False
    after: bool = False


class Guest(BaseModel):
    name: str
    phone: str
    presence: Presence
    food: Food
    alcohol: Alcohol
    transfer: Transfer

    def to_list(self) -> list:
        return [
            self.name,
            self.phone,
            str(self.presence) or "",
            str(self.food) or "",
            str(self.alcohol) or "",
            str(self.transfer) or "",
        ]
