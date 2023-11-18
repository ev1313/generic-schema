from generic_schema.validators import RegExValidator


class VersionValidator(RegExValidator):
    def __init__(self, name: str):
        super().__init__(name=name, regex=r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
