class Drone:
    drones: list["Drone"] = []

    def __init__(self, number: int, start: str):
        self.number: int = number
        self.path: list[str] = [start]
        Drone.drones.append(self)
