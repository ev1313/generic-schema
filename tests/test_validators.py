from generic_schema.validators import Int8Validator, Int16Validator, StringValidator, BooleanValidator, ArrayValidator
import pytest


def test_number_validators():
    schema = {"type": "int8", "min": 0, "max": 10}

    validator = Int8Validator("test")
    assert(validator.validate(5, schema))
    assert(validator.validate(10, schema))
    assert(validator.validate(0, schema))
    with pytest.raises(ValueError):
        validator.validate(-1, schema)
    with pytest.raises(ValueError):
        validator.validate(11, schema)


def test_string_validators():
    validator = StringValidator("test")
    assert(validator.validate("test", {}))

    schema = {"type": "string", "min": 4, "max": 10}

    validator = StringValidator("test")
    assert (validator.validate("test", schema))
    with pytest.raises(ValueError):
        validator.validate("tes", schema)
    with pytest.raises(ValueError):
        validator.validate("testtesttesttest", schema)


def test_boolean_validators():
    validator = BooleanValidator("test")

    assert(validator.validate(True, {}))
    assert(validator.validate(False, {}))


def test_array_validators():
    schema = {"subtype": "int8"}

    validator = ArrayValidator("test", Int8Validator("test_arrayitem"), {})

    assert(validator.validate([], schema))
    assert(validator.validate([1, 2, 3], schema))

    schema = {"subtype": "int8", "minlen": 1, "maxlen": 3}
    assert(validator.validate([1], schema))
    assert(validator.validate([1, 2, 3], schema))
    with pytest.raises(ValueError):
        assert(validator.validate([], schema))
    with pytest.raises(ValueError):
        assert(validator.validate([1, 2, 3, 4, 5, 6, 7], schema))
    # too big for int8
    with pytest.raises(ValueError):
        assert (validator.validate([1000], schema))
