import pytest

from generic_schema.extra_validators import VersionValidator, URIValidator
from generic_schema.parse_validator import parse_validator, validate_config
from generic_schema.validators import Int8Validator, Int16Validator, Int32Validator, Int64Validator, UInt8Validator, \
    UInt16Validator, UInt32Validator, UInt64Validator, FloatValidator, DoubleValidator, StringValidator, \
    BooleanValidator, ArrayValidator, RegExValidator, EMailValidator, FileValidator, DirectoryValidator


def test_parse_validator():
    int8validator = parse_validator("int8", {"_type": "int8"})
    assert(isinstance(int8validator, Int8Validator))
    assert(int8validator.name == "int8")

    int16validator = parse_validator("int16", {"_type": "int16"})
    assert(isinstance(int16validator, Int16Validator))
    assert(int16validator.name == "int16")

    int32validator = parse_validator("int32", {"_type": "int32"})
    assert(isinstance(int32validator, Int32Validator))
    assert(int32validator.name == "int32")

    int64validator = parse_validator("int64", {"_type": "int64"})
    assert(isinstance(int64validator, Int64Validator))
    assert(int64validator.name == "int64")

    uint8validator = parse_validator("uint8", {"_type": "uint8"})
    assert(isinstance(uint8validator, UInt8Validator))
    assert(uint8validator.name == "uint8")

    uint16validator = parse_validator("uint16", {"_type": "uint16"})
    assert(isinstance(uint16validator, UInt16Validator))
    assert(uint16validator.name == "uint16")

    uint32validator = parse_validator("uint32", {"_type": "uint32"})
    assert(isinstance(uint32validator, UInt32Validator))
    assert(uint32validator.name == "uint32")

    uint64validator = parse_validator("uint64", {"_type": "uint64"})
    assert(isinstance(uint64validator, UInt64Validator))
    assert(uint64validator.name == "uint64")

    floatvalidator = parse_validator("float", {"_type": "float"})
    assert(isinstance(floatvalidator, FloatValidator))
    assert(floatvalidator.name == "float")

    doublevalidator = parse_validator("double", {"_type": "double"})
    assert(isinstance(doublevalidator, DoubleValidator))
    assert(doublevalidator.name == "double")

    stringvalidator = parse_validator("string", {"_type": "string"})
    assert(isinstance(stringvalidator, StringValidator))
    assert(stringvalidator.name == "string")

    booleanvalidator = parse_validator("boolean", {"_type": "boolean"})
    assert(isinstance(booleanvalidator, BooleanValidator))
    assert(booleanvalidator.name == "boolean")

    arrayvalidator = parse_validator("array", {"_type": "array", "subtype": "int8"})
    assert(isinstance(arrayvalidator, ArrayValidator))
    assert(arrayvalidator.name == "array")

    regexvalidator = parse_validator("regex", {"_type": "regex"})
    assert(isinstance(regexvalidator, RegExValidator))
    assert(regexvalidator.name == "regex")

    emailvalidator = parse_validator("email", {"_type": "email"})
    assert(isinstance(emailvalidator, EMailValidator))
    assert(emailvalidator.name == "email")

    versionvalidator = parse_validator("version", {"_type": "version"})
    assert(isinstance(versionvalidator, VersionValidator))
    assert(versionvalidator.name == "version")

    filevalidator = parse_validator("file", {"_type": "file"})
    assert(isinstance(filevalidator, FileValidator))
    assert(filevalidator.name == "file")

    directoryvalidator = parse_validator("directory", {"_type": "directory"})
    assert(isinstance(directoryvalidator, DirectoryValidator))
    assert(directoryvalidator.name == "directory")

    urivalidator = parse_validator("uri", {"_type": "uri"})
    assert(isinstance(urivalidator, URIValidator))
    assert(urivalidator.name == "uri")

    with pytest.raises(TypeError):
        parse_validator("invalid", {"_type": "invalid"})

    with pytest.raises(TypeError):
        parse_validator("invalid", [])


def test_validate_config():
    schema = {"test1": {"_type": "int8", "min": 0, "max": 10},
              "test2": {"_type": "string"}}
    config = {"test1": 5, "test2": "test"}
    ret = validate_config(config, schema)

    assert(ret == config)

    config = {"test1": 5, "test2": 5}
    with pytest.raises(ValueError):
        validate_config(config, schema)

    config = {"test1": "str", "test2": "str2"}
    with pytest.raises(ValueError):
        validate_config(config, schema)

    schema = {"test1": {"_type": "int8", "min": 0, "max": 10},
              "test2": {"_type": "string"},
              "test3": {"test4": {"_type": "int8", "min": 0, "max": 10}}
              }
    config = {"test1": 5, "test2": "test", "test3": {"test4": 5}}
    ret = validate_config(config, schema)
    assert(ret == config)

    config = {"test1": 5, "test2": "test", "test3": {"test4": 11}}
    with pytest.raises(ValueError):
        validate_config(config, schema)

    config = {"test2": "test", "test3": {"test4": 11}}
    with pytest.raises(ValueError):
        validate_config(config, schema)

