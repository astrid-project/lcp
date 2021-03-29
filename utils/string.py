from string import Formatter as String_Formatter


class Formatter(String_Formatter):
    def convert_field(self, value, conversion):
        if 'c' == conversion:
            return value.capitalize()
        else:
            return super().convert_field(value, conversion)


format = Formatter().format


def is_str(obj):
    return isinstance(obj, str)
