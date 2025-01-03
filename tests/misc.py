from PIL import Image

from settings import settings

def patch_settings_file(*args):
    key_value_pairs = _args_tuple_to_dict(args)
    _update_settings(settings, key_value_pairs)

    return settings

def _args_tuple_to_dict(args):
    _dict, key = {}, None

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


class GuiControllerStub:

    def __init__(self, image_path):
        self._image = Image.open(image_path)

    def screenshot(self, region=None):
        if region is None:
            return self._image

        x1, y1 = region
        x2 = x1 + region[2]
        y2 = y1 + region[3]
        result_image = self._image.crop(box=(x1, y1, x2, y2))

        return result_image