# Generic Schema

Generic Schema is a validator library for making input validation of configuration files
easier.

## Installation

```bash
pip install generic-schema
```

## Usage

The schema and config are both dictionaries. The schema is a template for the config.
It is designed to load both from other file formats like TOML or JSON.

```python
from generic_schema.parse_validator import validate_config

schema = {
    "name": {"_type": "string", "minlen": 1, "maxlen": 10},
    "age": {"_type": "integer", "min": 0, "max": 100},
    "address": {
        "street": {"_type": "string", "minlen": 1, "maxlen": 10},
        "city": {"_type": "string", "minlen": 1, "maxlen": 10},
        "country": {"_type": "string", "minlen": 1, "maxlen": 10},
    }
}
config = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "Main Street",
        "city": "New York",
        "country": "USA",
    }
}

# validate whole configuration and schema,
# also asserts for missing keys in the configuration
validate_config(config, schema)

# it is also possible to only validate single values for specific keys
validate_config_key("address.country", "testtest", schema)
```

It is possible to check a type directly like this:

```python
from generic_schema.parse_validator import validate_type

schema = {"_type": "string", "minlen": 1, "maxlen": 10}
validate_type("hello", schema)
```