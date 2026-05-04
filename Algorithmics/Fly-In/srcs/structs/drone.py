class Drone:
    """Drone Docstring
    """
    drones: list["Drone"] = []

    def __init__(self, number: int, start: str):
        """A Drone numbered, and with its start position

        Args:
            number (int): _description_
            start (str): _description_
        """
        self.number: int = number
        self.path: list[str] = [start]
        Drone.drones.append(self)
