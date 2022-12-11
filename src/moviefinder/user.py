from moviefinder.item import ServiceName


class User:
    def __init__(self, name: str, email: str, region: str, services: list[ServiceName]):
        self.name = name
        self.email = email
        self.region = region
        self.services = services
