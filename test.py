import datetime
import io
import unittest
from unittest.mock import patch


import database
import work_log
import menu


class DbTests(unittest.TestCase):
    def setUp(self):
        database.init_db()
        delete = database.Entry.delete().where(database.Entry.id > 0)
        delete.execute()
        database.add_entry(name='miro 1', time=10,
                           task='task-1', notes='notes-2',
                           date=datetime.datetime(2019, 4, 1))
        database.add_entry(name='miro 2', time=20,
                           task='task-2', notes='notes-2',
                           date=datetime.datetime(2019, 4, 2))
        database.add_entry(name='miro 3', time=30,
                           task='task-3', notes='notes-3',
                           date=datetime.datetime(2019, 4, 3))
        database.add_entry(name='miro 4', time=30,
                           task='task-4', notes='notes-4',
                           date=datetime.datetime(2019, 4, 4))

    def test_add_entry(self):
        added = database.add_entry(name='miro 5', time=50,
                                   task='task-5', notes='notes-5')
        # check if one entry was added
        self.assertEqual(added, 1)
        entry = database.Entry.select().where(database.Entry.id == 5)
        for e in entry:
            self.assertEqual(e.name, 'miro 5')
            self.assertEqual(e.time, 50)
            self.assertEqual(e.task, 'task-5')
            self.assertEqual(e.notes, 'notes-5')

    def test_edit_entry(self):
        edited = database.edit_entry(3, time=350,
                                     task='task-35', notes='notes-35',
                                     date=datetime.datetime(2000, 1, 1))
        # check if one entry was edited
        self.assertEqual(edited, 1)
        entry = database.Entry.select().where(database.Entry.id == 3)
        for e in entry:
            self.assertEqual(e.time, 350)
            self.assertEqual(e.task, 'task-35')
            self.assertEqual(e.notes, 'notes-35')
            self.assertEqual(e.date, datetime.date(2000, 1, 1))

    def test_delete_entry(self):
        deleted = database.delete_entry(2)
        remaining = database.Entry.select().where(
            database.Entry.id > 0).count()
        # check if one entry was deleted
        self.assertEqual(deleted, 1)
        # number of remaining entries in database
        self.assertEqual(3, remaining)

    def test_search_by_range(self):
        entry_range = database.search_by_range(datetime.datetime(2019, 4, 2),
                                               datetime.datetime(2019, 4, 3))
        count = sum(1 for i in entry_range)
        # number of returned results
        self.assertEqual(count, 2)
        for e in entry_range:
            if e.id == 2:
                self.assertEqual(e.name, 'miro 2')
                self.assertEqual(e.time, 20)
                self.assertEqual(e.task, 'task-2')
                self.assertEqual(e.notes, 'notes-2')
            if e.id == 3:
                self.assertEqual(e.name, 'miro 3')
                self.assertEqual(e.time, 30)
                self.assertEqual(e.task, 'task-3')
                self.assertEqual(e.notes, 'notes-3')

    def test_search_by_time(self):
        result = database.search_by_time(30)
        count = sum(1 for i in result)
        # number of returned results
        self.assertEqual(count, 2)
        for e in result:
            if e.id == 3:
                self.assertEqual(e.name, 'miro 3')
                self.assertEqual(e.time, 30)
                self.assertEqual(e.task, 'task-3')
                self.assertEqual(e.notes, 'notes-3')
            if e.id == 4:
                self.assertEqual(e.name, 'miro 4')
                self.assertEqual(e.time, 30)
                self.assertEqual(e.task, 'task-4')
                self.assertEqual(e.notes, 'notes-4')

    def test_search_by_name(self):
        result = database.search_by_name('miro 1')
        count = sum(1 for i in result)
        # number of returned results
        self.assertEqual(count, 1)
        for e in result:
            if e.id == 1:
                self.assertEqual(e.name, 'miro 1')
                self.assertEqual(e.time, 10)
                self.assertEqual(e.task, 'task-1')
                self.assertEqual(e.notes, 'notes-2')

    def test_search_by_string(self):
        result = database.search_by_string('-2')
        count = sum(1 for i in result)
        # number of returned results
        self.assertEqual(count, 2)
        for e in result:
            if e.id == 1:
                self.assertEqual(e.name, 'miro 1')
                self.assertEqual(e.time, 10)
                self.assertEqual(e.task, 'task-1')
                self.assertEqual(e.notes, 'notes-2')
            if e.id == 2:
                self.assertEqual(e.name, 'miro 2')
                self.assertEqual(e.time, 20)
                self.assertEqual(e.task, 'task-2')
                self.assertEqual(e.notes, 'notes-2')


class WorkLogTests(unittest.TestCase):
    """
    Testing for simple console inputs and outputs. 
    Database functionality was already tested
    """

    def setUp(self):
        database.init_db()
        delete = database.Entry.delete().where(database.Entry.id > 0)
        delete.execute()
        database.add_entry(name='miro 1', time=10,
                           task='task-1', notes='notes-2',
                           date=datetime.datetime(2019, 4, 1))
        database.add_entry(name='miro 2', time=20,
                           task='task-2', notes='notes-2',
                           date=datetime.datetime(2019, 4, 2))
        database.add_entry(name='miro 3', time=30,
                           task='task-3', notes='notes-3',
                           date=datetime.datetime(2019, 4, 3))
        database.add_entry(name='miro 4', time=30,
                           task='task-4', notes='notes-4',
                           date=datetime.datetime(2019, 4, 4))

    def test_add_entry_success(self):
        user_input = [
            # correct
            'Miro 10',
            # correct
            'task-10',
            # incorrect
            'not allowed',
            # correct
            '500',
            # correct
            'notes-10'
        ]
        with patch('builtins.input', side_effect=user_input):
            success = work_log.add_entry()
            self.assertEqual(
                success, 'Entry successfully added to the database')
        entries = database.search_by_name('Miro 10')
        for e in entries:
            self.assertEqual(e.name, 'Miro 10')
            self.assertEqual(e.task, 'task-10')
            self.assertEqual(e.time, 500)
            self.assertEqual(e.notes, 'notes-10')

    def test_find_by_date_option_1(self):
        user_input = [
            # incorrect
            '3',
            # correct
            '1',
            # incorrect
            '10',
            # correct
            '1',
            # correct
            'notes-10'
        ]
        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_date()
        for e in entries:
            self.assertEqual(e.name, 'miro 1')
            self.assertEqual(e.task, 'task-1')
            self.assertEqual(e.time, 10)
            self.assertEqual(e.notes, 'notes-2')

    def test_find_by_date_option_2(self):
        user_input = [
            # incorrect
            '3',
            # correct
            '2',
            # incorrect
            '25/20/2020',
            '',
            # correct
            '1/4/2019',
            # correct
            '3/4/2019'
        ]
        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_date()
        count = 0
        for _ in entries:
            count = count + 1
        self.assertEqual(count, 3)

    def test_find_by_time_spent(self):
        user_input = [
            # incorrect
            'not a valid number',
            # correct
            '30'
        ]
        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_time_spent()
        # find_by_date is already tested in database
        count = 0
        for _ in entries:
            count = count + 1
        self.assertEqual(count, 2)

    def test_find_by_search_term(self):
        user_input = [
            '-2'
        ]
        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_search_term()
        # number of returned entries
        count = 0
        for _ in entries:
            count = count + 1
        self.assertEqual(count, 2)

    # https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_entry(self, mock_stdout):

        class entry():
            name = 'miro 1'
            task = 'task-1'
            time = 20
            date = datetime.date(2020, 2, 2)
            notes = 'notes-1'

        expected_output = (
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1'
        )

        work_log.print_entry(entry)
        self.assertEqual(mock_stdout.getvalue(), expected_output + '\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_entries_multiple(self, mock_stdout):

        class entry():
            name = 'miro 1'
            task = 'task-1'
            time = 20
            date = datetime.date(2020, 2, 2)
            notes = 'notes-1'

        expected_output = (
            'Result: 1 of 3\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n\n'
            'Result: 2 of 3\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n\n'
            'Result: 3 of 3\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n\n'
            'Result: 2 of 3\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n'
        )

        user_input = [
            # correct
            'N',
            # correct
            'N',
            # correct
            'P',
            # correct
            'B'
        ]
        
        entries = list()
        entries.append(entry)
        entries.append(entry)
        entries.append(entry)

        with patch('builtins.input', side_effect=user_input):
            work_log.display_entries(entries)
        value = mock_stdout.getvalue()
        self.maxDiff = None
        self.assertEqual(value, expected_output + '\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_entries_one_with_wrong_input_once(self, mock_stdout):

        class entry():
            name = 'miro 1'
            task = 'task-1'
            time = 20
            date = datetime.date(2020, 2, 2)
            notes = 'notes-1'

        expected_output = (
            'Result: 1 of 1\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n\n'
            'Result: 1 of 1\n\n'
            'name: miro 1\n'
            'task: task-1\n'
            'date: 2020-02-02\n'
            'time spent on task: 20\n'
            'notes: notes-1\n\n'
        )

        user_input = [
            # incorrect
            'F',
            # correct
            'B'
        ]

        entries = list()
        entries.append(entry)

        with patch('builtins.input', side_effect=user_input):
            work_log.display_entries(entries)
        value = mock_stdout.getvalue()
        self.maxDiff = None
        self.assertEqual(value, expected_output + '\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_display_entries_zero(self, mock_stdout):

        expected_output = (
            'No result found'
        )

        user_input = [
            ''
        ]

        entries = list()

        with patch('builtins.input', side_effect=user_input):
            work_log.display_entries(entries)
        value = mock_stdout.getvalue()
        self.maxDiff = None
        self.assertEqual(value, expected_output + '\n')

    def test_search_entries(self):
        user_input = [
            # incorrect
            '6',
            # correct
            '1'
        ]

        with patch('builtins.input', side_effect=user_input):
            answer = work_log.search_entries()
            self.assertEqual(answer, '1')

    def test_find_by_employee_option_one(self):
        user_input = [
            # incorrect
            '3',
            # correct
            '1',
            # incorrect
            '10',
            # correct
            '1'
        ]

        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_employee()
            count = 0
            for _ in entries:
                count = count + 1
            self.assertEqual(count, 1)

    def test_find_by_employee_option_two(self):
        user_input = [
            # correct
            '2',
            # correct
            'miro',
            # incorrect
            '10',
            # correct
            '2'
        ]

        with patch('builtins.input', side_effect=user_input):
            entries = work_log.find_by_employee()
            count = 0
            for _ in entries:
                count = count + 1
            self.assertEqual(count, 1)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_quit(self, mock_stdout):
        user_input = [
            # incorrect
            '5',
            # correct
            '3',
            ''
        ]
        expected_output = (
            'WORK LOG\n'
            'What whould you like to do?\n'
            'Option 5 is not in the menu. Please choose again.\n'
            'Thank you for using work log.\n'
        )
        with patch('builtins.input', side_effect=user_input):
            menu.menu()
            value = mock_stdout.getvalue()
            self.assertEqual(value, expected_output)


if __name__ == "__main__":
    unittest.main(exit=False)
