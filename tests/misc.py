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


class GuiControllerFake:

    def __init__(self, images_paths):
        self._images = [Image.open(img_path) for img_path in images_paths]
        self._clicks = []
        self._presses = []
        self._typewrites = []
        self._screenshot_call_count = 0

    def __del__(self):
        for img in self._images:
            img.close()

    @property
    def clicks(self):
        return self._clicks

    @property
    def presses(self):
        return self._presses

    @property
    def typewrites(self):
        return self._typewrites

    def screenshot(self, region=None):
        if len(self._images) == 1:
            img_idx = 0
        else:
            img_idx = self._screenshot_call_count

        if region is None:
            return self._images[img_idx]

        x1, y1, w, h = region
        x2, y2 = x1 + w, y1 + h
        result_image = self._images[img_idx]
        result_image = result_image.crop(box=(x1, y1, x2, y2))

        self._screenshot_call_count += 1

        return result_image

    def click(self, x, y):
        self._clicks.append((x, y))

    def press(self, key, repeat_count):
        self._presses.append((key, repeat_count))

    def typewrite(self, text):
        self._typewrites.append(text)