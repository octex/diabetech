from datetime import date
from flask import make_response


def registry_parser(registries):
    registries_list = []
    for registry in registries:
        registry_json = registry.to_json()
        registries_list.append(registry_json)
    return registries_list


def query_params_parser(query_params, possible_params):
    if len(query_params) == 0:
        return {}
    new_query_params = {}
    for param in query_params:
        if param in possible_params:
            new_query_params[param] = query_params[param]
    return new_query_params


def fecha_parser(fecha):
    fecha_content = fecha.split('-')
    if len(fecha_content) != 3:
        return make_response({"Error": "Date invalid format. Use AAAA-MM-DD"}, 406)
    year = int(fecha_content[0])
    month = int(fecha_content[1])
    day = int(fecha_content[2])
    new_date = date(year, month, day)
    return new_date
