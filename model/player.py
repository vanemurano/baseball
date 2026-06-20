from dataclasses import dataclass
from datetime import datetime


@dataclass
class Player():
    playerID: str
    birthCountry: str
    birthCity: str
    deathCountry: str
    deathCity: str
    nameFirst: str
    nameLast: str
    weight: int
    height: int
    bats: str
    throws: str
    birth_date: datetime
    debut_date: datetime
    finalgame_date: datetime
    death_date: datetime

    def __hash__(self):
        return hash(self.playerID)

    def __eq__(self, other):
        return self.playerID==other.playerID

    def __str__(self):
        return f"playerID = {self.playerID}, nome = {self.nameFirst}, cognome = {self.nameLast}"