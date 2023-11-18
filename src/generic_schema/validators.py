from typing import Any, List, Dict, Optional
import os, re

class Validator():
    def __init__(self, name: str):
        self.name = name

    def validate(self, value: Any, check: Dict[str, Any]) -> Optional[Any]:
        """
        Validates a value.
        :param value:
        :param check: Dictionary item loaded from the toml file
        :return:
        """
        if not "default" in check.keys():
            if value is None:
                raise ValueError(f"Missing field {self.name}")

            return value

        return check["default"]


class BooleanValidator(Validator):
    def __init__(self, name: str):
        super().__init__(name=name)

    def validate(self, value: Any, check: Dict[str, Any]) -> Optional[bool]:
        value = super().validate(value, check)

        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean")

        return value


class NumberValidator(Validator):
    def __init__(self, name: str, min = None, max = None):
        self.min = min
        self.max = max
        super().__init__(name=name)

    def validate(self, value: Optional[Any], check: Dict[str, Any]) -> Optional[bool]:
        """
        Validates a number value.
        :param value:
        :param check: Dictionary item loaded from the toml file
        :return:
        """
        value = super().validate(value, check)

        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number")

        # we either have a minimum from the datatype (like int8) or from the schema
        if self.min is not None:
            minimum = max(self.min, check.get("min", self.min))
        elif "min" in check.keys():
            minimum = check["min"]
        else:
            minimum = None
        if minimum is not None and value < minimum:
            raise ValueError("Value must be greater than {}".format(minimum))

        # we either have a maximum from the datatype (like int8) or from the schema
        if self.max is not None:
            maximum = min(self.max, check.get("max", self.max))
        elif "max" in check.keys():
            maximum = check["max"]
        else:
            maximum = None
        if maximum is not None and value > maximum:
            raise ValueError("Value must be less than {}".format(maximum))

        return value


class Int8Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=-128, max=127)


class Int16Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=-32768, max=32767)


class Int32Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=-2147483648, max=2147483647)


class Int64Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=-9223372036854775808, max=9223372036854775807)


class UInt8Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=0, max=255)


class UInt16Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=0, max=65535)


class UInt32Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=0, max=4294967295)


class UInt64Validator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name, min=0, max=18446744073709551615)


class FloatValidator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name)


class DoubleValidator(NumberValidator):
    def __init__(self, name: str):
        super().__init__(name=name)


class StringValidator(Validator):
    def __init__(self, name: str):
        super().__init__(name=name)

    def validate(self, value: Optional[str], check: Dict[str, Any]) -> Optional[str]:
        """
        Validates a string value.
        :param value:
        :param check: Dictionary item loaded from the toml file
        :return:
        """
        value = super().validate(value, check)

        if not isinstance(value, str):
            raise ValueError("Value must be a string")

        if "min" in check.keys() and len(value) < check["min"]:
            raise ValueError("Value must be at least {} characters long".format(check["min"]))

        if "max" in check.keys() and len(value) > check["max"]:
            raise ValueError("Value must be at most {} characters long".format(check["max"]))

        return value


class RegExValidator(StringValidator):
    def __init__(self, name: str, regex: Optional[str] = None):
        super().__init__(name=name)
        self.regex = regex

    def validate(self, value: Any, check: Dict[str, Any]) -> bool:
        """
        First validates a string value, then checks the string for the regular expression.
        :param value:
        :param check: Dictionary item loaded from the toml file
        :return:
        """
        value = super().validate(value, check)

        regex = check.get("regex", None)
        if regex is None:
            regex = self.regex
        if regex is None:
            raise ValueError("No regex specified")

        r = re.compile(regex)
        if not r.match(value):
            raise ValueError(f"RegEx '{regex}' does not match '{value}'")

        return value


class EMailValidator(Validator):
    def validate(self, value: Any, check: Dict[str, Any]) -> bool:
        value = super().validate(value, check)

        # from https://emailregex.com/index.html
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not pattern.match(value):
            raise ValueError(f"This is not a valid email address {value}")

        return value


class FileValidator(Validator):
    def validate(self, value: Any, check: Dict[str, Any]) -> bool:
        value = super().validate(value, check)

        if check.get("exists", True):
            if not os.path.exists(value):
                raise ValueError(f"File {value} does not exist")

        if check.get("isfile", True):
            if not os.path.isfile(value):
                raise ValueError(f"{value} is not a file")

        return value


class DirectoryValidator(Validator):
    def validate(self, value: Optional[str], check: Dict[str, Any]) -> Optional[str]:
        value = super().validate(value, check)

        if check.get("exists", True):
            if not os.path.exists(value):
                raise ValueError(f"File {value} does not exist")

        if check.get("isdir", True):
            if not os.path.isdir(value):
                raise ValueError(f"{value} is not a directory")

        return value


class ArrayValidator(Validator):
    def __init__(self, name: str, subtype: Validator, subtype_check: dict, minlen = None, maxlen = None):
        self.subtype = subtype
        self.subtype_check = subtype_check
        self.minlen = minlen
        self.maxlen = maxlen
        super().__init__(name)

    def validate(self, value: Optional[List], check: Dict[str, Any]) -> Optional[List]:
        value = super().validate(value, check)

        if not isinstance(value, list):
            raise ValueError(f"{self.name}: {value} is not a list")

        minlen = check.get("minlen", None)
        if minlen is not None:
            if len(value) < minlen:
                raise ValueError(f"{self.name}: {value} has not enough items ({minlen})")

        maxlen = check.get("maxlen", None)
        if maxlen is not None:
            if len(value) > maxlen:
                raise ValueError(f"{self.name}: {value} has too many items ({maxlen})")

        ret = []
        for v in value:
            ret.append(self.subtype.validate(v, self.subtype_check))

        return value


def parse_validator(name: str, check: Any) -> Validator:
    if isinstance(check, str):
        typename = check
    elif isinstance(check, dict):
        typename = check["_type"]
    else:
        raise TypeError(f"Invalid/Unknown check type {check}")

    if typename in ["float", "float32"]:
        return FloatValidator(name)
    elif typename in ["double", "float64"]:
        return DoubleValidator(name)
    elif typename in ["str", "string"]:
        return StringValidator(name)
    elif typename in ["int8", "char"]:
        return Int8Validator(name)
    elif typename in ["int16", "short"]:
        return Int16Validator(name)
    elif typename in ["int32", "int", "long"]:
        return Int32Validator(name)
    elif typename in ["int64", "long long"]:
        return Int64Validator(name)
    elif typename in ["uint8", "unsigned char", "byte"]:
        return UInt8Validator(name)
    elif typename in ["uint16", "unsigned short"]:
        return UInt16Validator(name)
    elif typename in ["uint32", "unsigned int", "unsigned long"]:
        return UInt32Validator(name)
    elif typename in ["uint64", "unsigned long long"]:
        return UInt64Validator(name)
    elif typename in ["bool", "boolean"]:
        return BooleanValidator(name)
    elif typename in ["email"]:
        return EMailValidator(name)
    elif typename in ["regex"]:
        return RegExValidator(name)
    elif typename in ["array", "arr"]:
        return ArrayValidator(name=name, subtype=parse_validator(name=f"{name}_arrayitem", check=check["subtype"]), subtype_check=check["subtype"] if isinstance(check["subtype"], dict) else {})
    else:
        raise TypeError(f"Invalid/Unknown typename {typename} for field {name}")


def validate_config(config: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates a configuration against a schema and returns the configuration.
    :param config: Dictionary containing the configuration
    :param schema: Dictionary containing the schema
    :return:
    """
    ret = {}
    for key, check in schema.items():
        if key not in config.keys():
            raise ValueError(f"Missing key {key} in config file")

        if isinstance(config[key], dict):
            ret[key] = validate_config(config[key], check)
            continue

        validator = parse_validator(name=key, check=check)
        ret[key] = validator.validate(config[key], check)

    return ret
