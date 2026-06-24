import dataclasses

import datetime


@dataclasses.dataclass
class State():
    id: str
    Name: str
    Capital: str
    Lat: float
    Lng: float
    Area: int
    Population:int
    Neighbors: str


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.Name