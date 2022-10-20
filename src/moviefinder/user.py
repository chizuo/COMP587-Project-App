class User:
    def __init__(self, name: str, email: str, country: str, services: list[str]):
        self.name = name
        self.email = email
        self.country = country
        self.services = services
