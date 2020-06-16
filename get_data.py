import sys


# Get all distinct dates on which there was a workout or workouts
def get_dates():
    dates = []
    for log in logs:
        ref = log.find('-')
        date = log[ref+2: ref+8].rstrip()
        if date not in dates:
            dates.append(date)
    return dates


# Get the number of workout days in a given month
def monthly_count(month):
    dates = get_dates()
    months = [date[:3] for date in dates]
    return months.count(month)


# Get all logs in a given month
def get_month(month):
    monthly_logs = []
    for log in logs:
        ref = log.find('-')
        mon = log[ref + 2: ref + 5]
        if mon == month:
            monthly_logs.append(log)
    return monthly_logs


# Get all logs on a given day (usually it's 1 log but sometimes there are multiple logs per day)
def get_day(date):
    date_logs = []
    for log in logs:
        ref = log.find('-')
        day = log[ref + 2: ref + 8].rstrip()
        if day == date:
            date_logs.append(log)
    return date_logs


# Get all logs for a given muscle since start of log
def get_muscle(muscle):
    group = []  # list of workouts for specified muscle
    for log in logs:
        mus = log[: log.find(' ')]
        if mus == muscle:
            group.append(log)
    return group


# AN ALTERNATIVE METHOD FOR EXTRACTING INFORMATION IS GENERATING A DATABASE-LIKE DICTIONARY, BUT IT'S MORE CONVOLUTED:
# def generate_database():
#     dates = get_dates()
#     dates_dict = {date: [] for date in dates}
#     for date in dates:
#         for log in logs:
#             ref = log.find('-')
#             day = log[ref+2: ref+9].rstrip()
#             if day == date:
#                 dates_dict[date].append(log)
#
#     months = set([day[:3] for day in dates])
#     months_dict = {month: {} for month in months}
#     for month in months:
#         for date, log in dates_dict.items():
#             if month == date[:3]:
#                 months_dict[month][int(date[4:])] = log
#
#     return months_dict


def main():
    global logs

    # Get list of logs (global b/c used by many functions)
    filename = 'gym_log.txt'
    with open(filename, 'r') as file:
        text = file.read()
        logs = text.split('\n\n\n')
        file.close()

    # Tell user which file is being used
    print(f'Getting information from file: {filename}\n')

    # Prompt user with info options
    print('[1] Total count')
    print('[2] Monthly count')
    print('[3] Get month')
    print('[4] Get day')
    print('[5] Get muscle')
    opt = input('>>> ')
    print()

    # Get total number of workout days since start of log
    if opt == '1':
        # Get info
        dates = get_dates()
        total = len(dates)

        # Display
        print(total, f'workout{"" if total == 1 else "s"} since', dates[0])

    # Get total number of workout days in a given month
    elif opt == '2':
        # Prompt user & format entry
        month = str(input('Enter month: '))[:3].title()

        # Get info
        count = monthly_count(month)

        # Display
        print()
        print(count, f'workout{"" if count == 1 else "s"} in', month)

    # Get all logs in a given month
    elif opt == '3':
        # Prompt user & format entry
        month = str(input('Enter month: '))[:3].title()

        # Get info
        monthly_logs = get_month(month)

        # Display
        if len(monthly_logs) == 0:
            print('\nNo workouts in', month)
        else:
            print('\n')
            print(*monthly_logs, sep='\n\n\n')

    # Get all logs on a given day (usually it's 1 log, but sometimes 2 logs were made for different muscles)
    elif opt == '4':
        # Prompt user & format entry
        date = str(input('Enter date: ')).title()
        try:
            month, day = date.split()
        except ValueError:
            print('\nInvalid date')
            sys.exit()
        month = month[:3]
        date = f'{month} {day}'

        # Get info
        date_logs = get_day(date)

        # Display
        if len(date_logs) == 0:
            print('\nNo workout on', date)
        else:
            print('\n')
            print(*date_logs, sep='\n\n\n')

    # Get all logs for a given muscle since start of log
    elif opt == '5':
        # Prompt user & format entry
        muscle = input('Enter muscle: ').upper()

        # Get info
        group = get_muscle(muscle)

        # Display
        if len(group) == 0:
            print(f'\nNo workouts for "{muscle}"')
        else:
            print('\n')
            print(*group, sep='\n\n\n')


main()
