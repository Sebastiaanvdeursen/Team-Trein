class Connection:
    def __init__(self, destination, time):
        self.destination = destination
        self.time = time
        self.done = False  # Nieuw attribuut om de status bij te houden