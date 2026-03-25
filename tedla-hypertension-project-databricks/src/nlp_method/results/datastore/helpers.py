from nlp_method.results import TABLE_SCHEMA


def results_field_list() -> str:
    return ", ".join([str(x) for x in list(TABLE_SCHEMA.keys())])
