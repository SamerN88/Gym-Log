import sys

# TODO: consider removing database fxn and writing simpler code that finds everything from 'logs' (like in get_muscle)


def get_workouts():
    global logs
    workouts = []
    for log in logs:
        workouts.append(log[: log.find('-')+9].rstrip())
    return workouts[:-1]


def get_days():
    global wo
    days_raw = [w[w.index('-')+2:] for w in wo]
    days_clean = []
    for day in days_raw:
        if day not in days_clean:
            days_clean.append(day)
    return days_clean


def monthly_count(month):
    months = [day[:3] for day in d]
    return months.count(month)


def get_muscle(muscle):
    muscle = muscle.upper()
    group = []  # list of workouts for specified muscle
    for log in logs:
        mus = log[:log.find(' ')]
        if mus == muscle:
            group.append(log)
    return group


def generate_database():
    days_dict = {day: [] for day in d}
    for day in d:
        for log in logs:
            if day == log[log.find('-')+2: log.find('-')+9].rstrip():
                days_dict[day].append(log)

    months = set([day[:3] for day in d])
    months_dict = {month: {} for month in months}
    for month in months:
        for day, log in days_dict.items():
            if month == day[:3]:
                months_dict[month][int(day[4:])] = log

    return months_dict


def main():
    print('[1] Total count')
    print('[2] Monthly count')
    print('[3] Get month')
    print('[4] Get day')
    print('[5] Get muscle')
    opt = input('>>> ')
    print()

    if opt == '1':
        print(len(d), f'workout{"" if len(d) == 1 else "s"} since', d[0])

    elif opt == '2':
        month = str(input('Enter month: '))[:3].title()
        count = monthly_count(month)
        print()
        print(count, f'workout{"" if count == 1 else "s"} in', month)

    elif opt == '3':
        month = str(input('Enter month: '))[:3].title()
        print()
        try:
            info = [log for day in database[month].values() for log in day]
            print()
            print(*info, sep='\n\n\n')
        except KeyError:
            print('No workout on', month)

    elif opt == '4':
        date = str(input('Enter date: ')).title()

        try:
            month, day = date.split()
        except ValueError:
            print('\nInvalid date')
            sys.exit()

        month = month[:3]
        date = f'{month} {day}'

        print()
        try:
            info = database[month][int(day)]
            print()
            print(*info, sep='\n\n\n')
        except KeyError:
            print('No workout on', date)

    elif opt == '5':
        muscle = input('Enter muscle: ')
        group = get_muscle(muscle)
        if len(group) == 0:
            print(f'\nNo workouts for "{muscle}"')
        else:
            print('\n')
            print(*group, sep='\n\n\n')


filename = 'gym_log.txt'
with open(filename, 'r') as file:
    text = file.read()
    logs = text.split('\n\n\n')
    file.close()

wo = get_workouts()
d = get_days()
database = generate_database()

main()
