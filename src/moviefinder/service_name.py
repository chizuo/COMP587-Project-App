import enum


class ServiceName(enum.Enum):
    AMAZON_PRIME = "prime"
    APPLE_TV_PLUS = "apple"
    DISNEY_PLUS = "disney"
    HULU = "hulu"
    NETFLIX = "netflix"

    @classmethod
    def contains(cls, value: str) -> bool:
        """Returns True if the given ServiceName value is in the enum."""
        return value in (e.value for e in cls.__members__.values())
