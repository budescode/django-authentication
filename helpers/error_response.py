
def custom_error_msg(error):
    try:
        keys = error
        dict_pairs = keys.items()
        pairs_iterator = iter(dict_pairs)
        first_pair = next(pairs_iterator)
        key1 = first_pair[0]
        message1 = first_pair[1][0]
        error_str = f'{key1}: {message1}'
        return error_str
    except:
        return str(error)