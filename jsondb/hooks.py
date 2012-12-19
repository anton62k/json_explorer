# coding: utf8


def hook_int_float(pattern, old_value, new_value):
    if pattern.values and not new_value in pattern.values:
        return old_value

    if not pattern.min == None and new_value < pattern.min:
        return old_value

    if not pattern.max == None and new_value > pattern.max:
        return old_value

    return new_value


def hook_str(pattern, old_value, new_value):
    if pattern.values and not new_value in pattern.values:
        return old_value
    return new_value


def hook_incr(pattern, old_value, new_value):
    if not old_value and not new_value:
        return pattern.project.values.incr(pattern.incr)
    if not old_value and new_value:
        return new_value
    return old_value
