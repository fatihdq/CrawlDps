def progress_bar(current, total, bar_length=50):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {current}/{total} ({int(fraction*100)}%)', end=ending)