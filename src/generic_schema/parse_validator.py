from typing import Any, Dict

from generic_schema.extra_validators import VersionValidator, URIValidator
from generic_schema.validators import Validator, FloatValidator, DoubleValidator, StringValidator, Int8Validator, \
    Int16Validator, Int32Validator, Int64Validator, UInt8Validator, UInt16Validator, UInt32Validator, UInt64Validator, \
    BooleanValidator, EMailValidator, RegExValidator, FileValidator, DirectoryValidator, ArrayValidator


def parse_validator(name: str, check: Any) -> Validator:
    """
    returns a validator instance for the given check
    :param name: name of the field
    :param check: check dictionary to parse (_type field determines instance type)
    :return:
    """
    if isinstance(check, str):
        typename = check
    elif isinstance(check, dict):
        typename = check.get("_type", None)
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
    elif typename in ["version"]:
        return VersionValidator(name)
    elif typename in ["file"]:
        return FileValidator(name)
    elif typename in ["directory", "dir"]:
        return DirectoryValidator(name)
    elif typename in ["uri"]:
        return URIValidator(name)
    elif typename in ["array", "arr"]:
        return ArrayValidator(name=name, subtype=parse_validator(name=f"{name}_arrayitem", check=check["subtype"]), subtype_check=check["subtype"] if isinstance(check["subtype"], dict) else {})
    else:
        raise TypeError(f"Invalid/Unknown typename {typename} for field {name}")


def validate_type(value: Any, check: Any) -> Any:
    """
    Validates a single value against a check.
    :param value:
    :param check: Dictionary item loaded from the toml file, may be dictionary or string
    :return:
    """
    validator = parse_validator(name="value", check=check)
    return validator.validate(value=value, check=check)


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
            try:
                ret[key] = validate_config(config[key], check)
                continue
            except ValueError as e:
                raise ValueError(f"Error in subfield of {key}: {e}") from e

        try:
            ret[key] = validate_type(value=config[key], check=check)
        except ValueError as e:
            raise ValueError(f"Error in field {key}: {e}") from e

    return ret


def validate_config_key(key: str, value: Any, schema: Dict[str, Any]) -> Any:
    """
    Validates a single key against a schema and returns the value.

    :param key: Key to validate, may be in format "key.subkey.subsubkey"
    :param value: Value to validate
    :param schema: Dictionary containing the schema
    :return:
    """

    # first get the schema for the key
    check = schema
    for key_part in key.split("."):
        if key_part not in check.keys():
            raise ValueError(f"Missing key {key} in schema")
        check = check[key_part]

    return validate_type(value=value, check=check)

