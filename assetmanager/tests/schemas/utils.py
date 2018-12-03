# -*- coding: utf-8 -*-
import json
from os.path import join, dirname

# modified from https://medium.com/grammofy/testing-your-python-api-app-with-json-schema-52677fe73351
def load_json_schema(filename):
    """ Loads the given schema file """
    absolute_path = join(dirname(__file__), filename)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())
