def deep_get(dictionary, field_path, default=None):
    keys = field_path.split('.')
    for key in keys:
        if dictionary is None or key not in dictionary:
            return default
        dictionary = dictionary[key]
    return dictionary