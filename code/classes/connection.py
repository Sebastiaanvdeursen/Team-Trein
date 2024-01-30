class Connection:
    def __init__(self, destination: str, time: int) -> None:
        """
        Initialize a Connection instance.

        pre:
        - destination is a string representing the destination of the connection.
        - time is an integer representing the time it takes for the connection.
        """
        self.destination = destination
        self.time = time
        self.done = False
