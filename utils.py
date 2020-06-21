def human_to_bytes(human):
    value, unit = human.split(" ")
    value = float(value.replace(",", "."))

    if unit == "B":
        pass
    elif unit == "KB":
        value*1e3
    elif unit == "MB":
        value*1e6
    elif unit == "GB":
        value*1e9
    elif unit == "TB":
        value*1e12
    else:
        raise ValueError(f"Unknown human format: {human!r}")

    return value
