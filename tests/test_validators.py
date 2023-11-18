from generic_schema.validators import NumberValidator, FloatValidator, DoubleValidator, Int8Validator, Int16Validator, \
    Int32Validator, Int64Validator, UInt8Validator, UInt16Validator, UInt32Validator, UInt64Validator, StringValidator, \
    BooleanValidator, ArrayValidator, RegExValidator, EMailValidator, parse_validator
import pytest


def test_number_validators():
    schema = {"_type": "int8", "min": 0, "max": 10}

    validator = Int8Validator("test")
    assert(validator.validate(5, schema) == 5)
    assert(validator.validate(10, schema) == 10)
    assert(validator.validate(0, schema) == 0)
    with pytest.raises(ValueError):
        validator.validate(-1, schema)
    with pytest.raises(ValueError):
        validator.validate(11, schema)
    with pytest.raises(ValueError):
        validator.validate("test", schema)


    validator = NumberValidator("test")
    assert(validator.validate(5, schema) == 5)
    assert(validator.validate(10, schema) == 10)
    assert(validator.validate(0, schema) == 0)
    with pytest.raises(ValueError):
        validator.validate(-1, schema)
    with pytest.raises(ValueError):
        validator.validate(11, schema)
    with pytest.raises(ValueError):
        validator.validate("test", schema)


    validator = NumberValidator("test", min=0, max=10)
    assert(validator.validate(5, {}) == 5)
    assert(validator.validate(10, {}) == 10)
    assert(validator.validate(0, {}) == 0)
    with pytest.raises(ValueError):
        validator.validate(-1, {})
    with pytest.raises(ValueError):
        validator.validate(11, {})
    with pytest.raises(ValueError):
        validator.validate("test", {})

    validator = NumberValidator("test")
    assert(validator.validate(5, {}) == 5)
    assert(validator.validate(10, {}) == 10)
    assert(validator.validate(0, {}) == 0)
    assert(validator.validate(-1, {}) == -1)
    assert(validator.validate(11, {}) == 11)
    with pytest.raises(ValueError):
        validator.validate("test", {})


    validator = Int8Validator("test")
    assert(validator.min == -128)
    assert(validator.max == 127)
    validator = Int16Validator("test")
    assert(validator.min == -32768)
    assert(validator.max == 32767)
    validator = Int32Validator("test")
    assert(validator.min == -2147483648)
    assert(validator.max == 2147483647)
    validator = Int64Validator("test")
    assert(validator.min == -9223372036854775808)
    assert(validator.max == 9223372036854775807)

    validator = UInt8Validator("test")
    assert(validator.min == 0)
    assert(validator.max == 255)
    validator = UInt16Validator("test")
    assert(validator.min == 0)
    assert(validator.max == 65535)
    validator = UInt32Validator("test")
    assert(validator.min == 0)
    assert(validator.max == 4294967295)
    validator = UInt64Validator("test")
    assert(validator.min == 0)
    assert(validator.max == 18446744073709551615)

    validator = FloatValidator("test")
    assert(validator.validate(0, {"min": 0, "max": 1.5}) == 0)
    assert(validator.validate(0.6, {"min": 0, "max": 1.5}) == 0.6)
    assert(validator.validate(1.2, {"min": 0, "max": 1.5}) == 1.2)
    with pytest.raises(ValueError):
        validator.validate(1.52, {"min": 0, "max": 1.5})

    validator = DoubleValidator("test")
    assert(validator.validate(0, {"min": 0, "max": 1.5}) == 0)
    assert(validator.validate(0.6, {"min": 0, "max": 1.5}) == 0.6)
    assert(validator.validate(1.2, {"min": 0, "max": 1.5}) == 1.2)
    with pytest.raises(ValueError):
        validator.validate(1.52, {"min": 0, "max": 1.5})


def test_string_validators():
    validator = StringValidator("test")
    assert(validator.validate("test", {}))

    schema = {"_type": "string", "min": 4, "max": 10}

    validator = StringValidator("test")
    assert (validator.validate("test", schema) == "test")
    with pytest.raises(ValueError):
        validator.validate("tes", schema)
    with pytest.raises(ValueError):
        validator.validate("testtesttesttest", schema)
    with pytest.raises(ValueError):
        validator.validate(13, schema)


def test_boolean_validators():
    validator = BooleanValidator("test")

    assert(validator.validate(True, {})) == True
    assert(validator.validate(False, {})) == False

    with pytest.raises(ValueError):
        validator.validate(None, {})

    with pytest.raises(ValueError):
        validator.validate(1, {})


def test_array_validators():
    schema = {"subtype": "int8"}

    validator = ArrayValidator("test", Int8Validator("test_arrayitem"), {})

    assert(validator.validate([], schema) == [])
    assert(validator.validate([1, 2, 3], schema) == [1, 2, 3])

    schema = {"subtype": "int8", "minlen": 1, "maxlen": 3}
    assert(validator.validate([1], schema) == [1])
    assert(validator.validate([1, 2, 3], schema) == [1, 2, 3])
    with pytest.raises(ValueError):
        assert(validator.validate([], schema))
    with pytest.raises(ValueError):
        assert(validator.validate([1, 2, 3, 4, 5, 6, 7], schema))
    # too big for int8
    with pytest.raises(ValueError):
        assert (validator.validate([1000], schema))

    with pytest.raises(ValueError):
        assert(validator.validate({}, schema))


def test_regex_validators():
    schema = {"_type": "regex", "regex": "^[a-z]+$"}

    validator = RegExValidator("test")
    assert(validator.validate("test", schema) == "test")
    with pytest.raises(ValueError):
        validator.validate("TEST", schema)
    with pytest.raises(ValueError):
        validator.validate("test1", schema)
    with pytest.raises(ValueError):
        validator.validate(13, schema)
    with pytest.raises(ValueError):
        validator.validate("asdf", {"_type": "regex"})


def test_email_validators():
    validator = EMailValidator("test")

    assert(validator.validate("test@example.com", {}) == "test@example.com")
    assert(validator.validate("test+test@example.com", {}) == "test+test@example.com")

    with pytest.raises(ValueError):
        validator.validate("test", {})


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

    with pytest.raises(TypeError):
        parse_validator("invalid", {"_type": "invalid"})

    with pytest.raises(TypeError):
        parse_validator("invalid", [])


def test_default_key_validator():
    schema = {"_type": "int8", "min": 0, "max": 10, "default": 5}

    validator = Int8Validator("test")
    assert(validator.validate(None, schema) == 5)

    schema = {"_type": "int8", "min": 0, "max": 10}
    with pytest.raises(ValueError):
        validator.validate(None, schema)


def test_validate_config():
    schema = {"test1": {"type": "int8", "min": 0, "max": 10},
              "test2": {"type"}}
