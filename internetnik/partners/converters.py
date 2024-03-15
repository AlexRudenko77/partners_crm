def to_python(value):
    return int(value)


def to_url(value):
    return "%04d" % value


class FourDigitYearConverter:
    regex = "[0-9]{4}"

