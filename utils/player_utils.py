from classes.bcolors import bcolors


def generate_label(string, suffix, end_spaces):
    return bcolors.BOLD + string + suffix + end_spaces + bcolors.ENDC


def generate_stat_bar(current_stat, max_stat, width, color):
    stat_ending = " "

    stat = bcolors.BOLD + str(current_stat) + "/" + str(max_stat) + stat_ending + bcolors.ENDC
    stat_bar = "|" + color + generate_bar(current_stat, max_stat, width) + bcolors.ENDC + "|"

    return stat + stat_bar


def generate_bar(current, stat_max, bar_spaces):
    bars = ""
    bar_ticks = int(round(current / stat_max * 100 / (100 / bar_spaces)))
    for i in range(bar_spaces):
        if i + 1 <= bar_ticks:
            bars += "█"
        else:
            bars += " "
    return bars


def generate_spaces(max_characters, current_characters):
    remaining_spaces = max_characters - current_characters
    spaces = ""
    for i in range(remaining_spaces):
        spaces += " "
    return spaces
