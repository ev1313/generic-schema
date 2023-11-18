from generic_schema.validators import RegExValidator


class VersionValidator(RegExValidator):
    """
    Validates a version string of the form major.minor.patch
    """

    def __init__(self, name: str):
        super().__init__(name=name, regex=r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


class URIValidator(RegExValidator):
    """
    Validates a URL of the form scheme://netloc/path;parameters?query#fragment as defined in RFC 2396.

    Groups are:
      scheme    = $2
      authority = $4
      path      = $5
      query     = $7
      fragment  = $9
    """
    def __init__(self, name: str):
        super().__init__(name=name, regex=r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$")
