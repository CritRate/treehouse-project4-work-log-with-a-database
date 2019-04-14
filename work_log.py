import database

import datetime

from clear_console import clear


def add_entry():
    name = input('Enter name:')
    clear()
    task = input('Enter task name:')
    clear()
    while(True):
        str_time = input('Enter number of minutes spent on the task:')
        clear()
        try:
            int_time = int(str_time)
            break
        except ValueError:
            print('Cannot be converted to number. Please try again.')
            continue
    clear()
    notes = input('Enter any additional notes:')
    clear()
    database.add_entry(
        name=name, time=int_time, task=task, notes=notes)
    return 'Entry successfully added to the database'


def search_entries():
    clear()
    print('Choose search option:')
    while True:
        answer = input(
            '1: Find by employee \n' +
            '2: Find by date \n' +
            '3: Find by minutes spents \n' +
            '4: Find by search term \n')
        if answer in '1234':
            break
        else:
            clear()
            print(f'Option {answer} is not in the menu. Please choose again.')
            continue
    clear()
    return answer


def find_by_employee():
    clear()
    print('Search by:')
    while True:
        answer = input(
            '1: list of all employee entries \n' +
            '2: writing the name of an employee \n')
        if answer in '12':
            break
        else:
            clear()
            print(f'Option {answer} is not in the menu. Please choose again.')
            continue
    clear()
    if answer == '1':
        unique_employees = database.Entry.select(
            database.Entry.name).distinct()
        options = ''
        employees = list()
        for count, emp in enumerate(unique_employees, 1):
            employees.append(emp.name)
            options += f'{count}: {emp.name}\n'
        while True:
            print('Choose the employee:')
            answer = input(options)
            try:
                option = int(answer)
                if option > len(employees):
                    raise ValueError
            except ValueError:
                clear()
                print(
                    f'Option {answer} is not in the menu. Please choose again.')
                continue
            break
        clear()
        entries = database.Entry.select().where(
            database.Entry.name == employees[option - 1])
        return entries
    if answer == '2':
        search_term = input('Please enter name of the employee: ')
        # seach for all the unique employees
        unique_employees = database.Entry.select(database.Entry.name).where(
            database.Entry.name.contains(search_term)).distinct()
        options = ''
        employees = list()
        # make list of unique employees
        for count, emp in enumerate(unique_employees, 1):
            employees.append(emp.name)
            options += f'{count}: {emp.name}\n'
        while True:
            if len(employees) == 1:
                option = 1
                break
            clear()
            print('Choose the employee:')
            answer = input(options)
            try:
                option = int(answer)
                if option > len(employees):
                    raise ValueError
            except ValueError:
                clear()
                print(
                    f'Option {answer} is not in the menu. Please choose again')
                continue
            break
        entries = database.search_by_name(employees[option - 1])
        return entries


def find_by_date():
    while True:
        answer = input(
            '1: find by list of dates \n' +
            '2: find by listing range of dates \n')
        if answer in '12':
            break
        else:
            clear()
            print(f'Option {answer} is not in the menu. Please choose again.')
            continue
    if answer == '1':
        clear()
        unique_dates = database.Entry.select(
            database.Entry.date).distinct()
        options = ''
        dates = list()
        # list of dates to choose from
        for count, date in enumerate(unique_dates, 1):
            dates.append(date.date)
            options += f'{count}: {date.date}\n'
        while True:
            print('Choose the Date:')
            answer = input(options)
            try:
                option = int(answer)
                if option > len(dates):
                    raise ValueError
            except ValueError:
                clear()
                print(
                    f'Option {answer} is not in the menu. Please choose again')
                continue
            break
        option = option - 1
        entries = database.search_by_range(dates[option], dates[option])
        clear()
        return entries
    if answer == '2':
        clear()
        while True:
            try:
                print('Enter the date range')
                date1 = input('Please use DD/MM/YYYY date #1: ')
                valid_date1 = datetime.datetime.strptime(date1, '%d/%m/%Y')
                date2 = input('Please use DD/MM/YYYY date #2: ')
                valid_date2 = datetime.datetime.strptime(date2, '%d/%m/%Y')
                break
            except ValueError:
                print('One of the date are not a valid date')
                input('Press enter to try again')
                clear()
                continue
        entries = database.search_by_range(valid_date1, valid_date2)
        return entries


def find_by_time_spent():
    clear()
    while(True):
        str_time = input('Enter number of minutes spent on the task:')
        clear()
        try:
            int_time = int(str_time)
            break
        except ValueError:
            print('Cannot be converted to number. Please try again.')
            continue
    clear()
    entries = database.search_by_time(int_time)
    return entries


def find_by_search_term():
    clear()
    search_term = input('Enter the search term: ')
    entries = database.search_by_string(search_term)
    return entries


def print_entry(entry):
    print((
        f'name: {entry.name}\n'
        f'task: {entry.task}\n'
        f'date: {entry.date}\n'
        f'time spent on task: {entry.time}\n'
        f'notes: {entry.notes}'
    ))


def display_entries(entries):
    list_entries = list()
    if entries:
        for entry in entries:
            list_entries.append(entry)

    index = 0
    while(True):
        while(True):
            clear()
            if(len(list_entries) == 0):
                print('No result found')
                input()
                return
            print(f'Result: {index + 1} of {len(list_entries)}\n')
            print_entry(list_entries[index])
            print('\n')
            if len(list_entries) == 1:
                choice = input('[B]ack\n')
            elif index == 0:
                choice = input('[N]ext, [B]ack\n')
            elif len(list_entries) - 1 == index:
                choice = input('[P]revious, [B]ack\n')
            else:
                choice = input('[P]revious, [N]ext, [B]ack\n')
            choice = choice.upper()
            if choice in 'PNB':
                break
            else:
                continue
        if choice == 'N' and index < len(list_entries) - 1:
            index = index + 1
        if choice == 'P' and index > 0:
            index = index - 1
        if choice == 'B':
            break
