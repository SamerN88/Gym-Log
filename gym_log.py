import textwrap


def prepare_file():
    global write
    global file
    global pl

    log_to_file = input('Log to file? [Y/N]: ').lower()
    if log_to_file in ['y', 'yes']:
        write = True
        file = open(filename, 'a')

        muscle = input('\nMuscle area: ')
        date = input('Date: ')
        pl = input('Previous load: ')

        file.write(f"{muscle.upper()} - {date.title()}".ljust(35) + (f'PL: {pl}'.rjust(30) if pl != '' else '') + '\n')
        file.write('Exercise'.ljust(30) + 'Weight'.rjust(10) + 'Reps'.rjust(10) + 'Load'.rjust(15) + '\n')
        file.write('¯'*65 + '\n')
    else:
        write = False


def workout():
    global pl

    print()

    ex_loads = []
    new_exercise = input()

    while new_exercise != '':
        log(new_exercise, 'e')

        set_loads = []
        new_set = input()

        while new_set != '':
            if new_set[-1].isdigit() is False:
                symbol = new_set[-1]
                note = input(symbol + ' ')
                new_set = new_set[:-1]
            else:
                symbol = ''
                note = ''

            weight, reps = [int(e) for e in new_set.split()]
            load = weight * reps
            set_loads.append(load)

            print(' '*7, load)
            log(weight, 'w', (symbol, note))
            log(reps, 'r')
            log(load, 'l', (symbol, note))

            new_set = input()

        ex_load = sum(set_loads)
        ex_loads.append(ex_load)

        print('—'*7, ex_load, '\n')
        log(ex_load, 'el')

        new_exercise = input()

    total_load = sum(ex_loads)

    try:
        if pl != '':
            pl = int(pl)
            diff = int(total_load) - pl
            progress = f' ({diff if diff < 0 else "+" + str(diff)})'
        else:
            progress = ''
    except NameError:
        progress = ''

    print(f'Total load: {total_load}{progress}\n')
    final_notes = input('Final notes: ')

    log(total_load, 'tl', ('', final_notes))


def log(value, kind, symbol_note=('', '')):
    global first_set
    global pl

    if write is False:
        return

    value = str(value)

    if kind == 'e':
        first_set = True
        file.write(value.ljust(30))
    elif kind == 'w':
        symbol = symbol_note[0]
        if symbol == '':
            symbol = ' '

        if first_set:
            file.write(value.rjust(10) + ' ' + symbol)
        else:
            file.write(' '*30 + value.rjust(10) + ' ' + symbol)
        first_set = False
    elif kind == 'r':
        file.write(value.rjust(8))
    elif kind == 'l':
        symbol, note = symbol_note
        if symbol + note in ['', symbol]:
            symbol_and_note = ''
        else:
            symbol_and_note = f'  {symbol} {note}'

        file.write(value.rjust(15) + symbol_and_note + '\n')
    elif kind == 'el':
        file.write(('= ' + value).rjust(65) + '\n\n')
    elif kind == 'tl':
        if pl != '':
            pl = int(pl)
            diff = int(value) - pl
            progress = f' ({diff if diff < 0 else "+" + str(diff)})'
        else:
            progress = ''

        notes = symbol_note[1]
        if notes != '':
            if len(notes) > 65:
                wrap_notes = textwrap.wrap(notes, 65)
                notes = '\n'.join(line for line in wrap_notes)
            else:
                notes = notes.center(65)

        file.write(f'Total load: {value}{progress}'.center(65) + ('\n' if notes != '' else '') + notes + '\n\n\n')


def main():
    prepare_file()
    workout()

    if write:
        file.close()


filename = 'gym_log.txt'
main()
