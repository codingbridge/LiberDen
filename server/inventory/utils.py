# pylint: disable=missing-docstring

def get_name_value_pair(search):
    if ':' in search:
        name, value = search.split(':')
    else:
        name = ""
        value = search

    return name, value

def get_search_keywords_dict(search_string):
    result = {}
    search_string = search_string.lower()
    if '|' in search_string:
        sub_strings = search_string.split('|')
        for sub in sub_strings:
            name, value = get_name_value_pair(sub)
            if name in result:
                result[name].append(value)
            else:
                result[name] = [value]
    else:
        name, value = get_name_value_pair(search_string)
        if name in result:
                result[name].append(value)
        else:
            result[name] = [value]

    return result

