import sys

sys.path.append('src')

from settings import settings

def patch_settings_file(*args):
    key_value_pairs = _args_tuple_to_dict(args)
    _update_settings(settings, key_value_pairs)

    return settings

def _args_tuple_to_dict(args):
    _dict = {}

    for i, v in enumerate(args):
        if i % 2 == 0:
            key = v
        else:
            _dict[key] = v

    return _dict

def _update_settings(settings, key_value_pairs):
    for key, value in key_value_pairs.items():
        _update_setting(settings, key, value)

def _update_setting(settings, key, value):
    s = settings
    key_tokens = key.split('.')

    for t in key_tokens[:-1]:
        s = s[t]

    s[key_tokens[-1]] = value