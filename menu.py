from clear_console import clear
import work_log
import database


def menu():
    database.init_db()
    while True:
        clear()
        print('WORK LOG')
        print('What whould you like to do?')
        while True:
            answer = input((
                '1: Add new entry\n'
                '2: Search in existing entries\n'
                '3: Quit Program\n'
            ))
            if answer in '123':
                break
            else:
                clear()
                print(
                    f'Option {answer} is not in the menu. Please choose again.')
                continue
        clear()
        if answer == '1':
            input(work_log.add_entry())
        if answer == '2':
            search_option = work_log.search_entries()
            if search_option == '1':
                work_log.display_entries(work_log.find_by_employee())
            if search_option == '2':
                work_log.display_entries(work_log.find_by_date())
            if search_option == '3':
                work_log.display_entries(work_log.find_by_time_spent())
            if search_option == '4':
                work_log.display_entries(work_log.find_by_search_term())
        if answer == '3':
            print('Thank you for using work log.')
            input()
            break
