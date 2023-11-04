import json
import tomllib
import argparse

from validators import parse_validator, Validator

import pdb


def load_schema(schema: dict, path: str = "") -> dict:
    ret = {}
    if len(path) > 0:
        path += "."

    for k, v in schema.items():
        if isinstance(v, dict):
            if v.get("_type", None) is not None:
                ret[k] = parse_validator(path + k, v)
            else:
                ret[k] = load_schema(v, path + k)
        elif isinstance(v, str):
            ret[k] = parse_validator(path + k, v)
        else:
            raise TypeError(f"Unsupported type in schema {type(v)}")

    return ret


def check_schema(config: dict, schema: dict, schema_data: dict):
    for k, v in schema:
        if isinstance(v, Validator):
            v.validate(config[k], schema_data[k])
        elif isinstance(v, dict):
            if config is None:
                config = {}
            check_schema(config.get(k, None), v, schema_data[k])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="config file to check")
    parser.add_argument("-s", "--schema", help="schema file to use")
    args = parser.parse_args()

    configfile = open(args.file, "r")
    config_data = json.load(configfile)

    with open(args.schema, "rb") as f:
        schema_data = tomllib.load(f)
        schema = load_schema(schema_data)

    check_schema(config_data, schema, schema_data)
    pdb.set_trace()