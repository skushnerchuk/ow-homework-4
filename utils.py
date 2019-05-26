import os


def is_correct_ext(filename, extensions):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    return ext in [x.lower() for x in extensions]
