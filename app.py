from models import (Base, session,
                    Book, engine)
import csv
import datetime
import time
import utils


def menu():
    while True:
        print('''
              \nPROGRAMMING BOOKS
              \r1) Add book
              \r2) View all books
              \r3) Search for book
              \r4) Book Analysis
              \r5) Exit
              ''')
        choice = input('What would you like to do?\n> ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                  \nInvalid input. Choose one of the options above.
                  \rA number from 1-5.
                  \rPress ENTER to try again.
                  ''')


def submenu():
    while True:
        print('''
              \r1) Edit
              \r2) Delete
              \r3) Return to Main Menu 
              ''')
        choice = input('What would you like to do?\n> ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
                  \nInvalid input. Choose one of the options above.
                  \rA number from 1-3.
                  \rPress ENTER to try again.
                  ''')


def clean_id(id_str, id_options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
              \n ******ID ERROR******
              \rThe price should be a number.
              \rPress Enter to try again.
              \r*********************
              ''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input(f'''
                  \n ******ID ERROR******
                  \rOptions: {id_options}
                  \rPress Enter to try again.
                  \r*********************
                  ''')
            return


def edit_check(column_name, current_value):
    print(f'\n***** EDIT {column_name} *****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value / 100}')
    elif column_name == 'Published':
        print(f'\rCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'Current Value: {current_value}')

    if column_name == 'Published' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to: ')
            if column_name == 'Published':
                changes = utils.clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = utils.clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to: ')


def add_csv():
    with open('suggested_books.csv', 'r') as file:
        data = csv.reader(file)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = utils.clean_date(row[2])
                price = utils.clean_price(row[3])
                new_book = Book(title=title, author=author,
                                published_date=date, price=price)
                session.add(new_book)
        session.commit()
        time.sleep(1)
        print('Book added!')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex. October 25, 2017): ')
                date = utils.clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex. 29.99): ')
                price = utils.clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author,
                            published_date=date, price=price)
            session.add(new_book)
            session.commit()
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress Enter to go back to Main Menu.')
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice= input(f'''
                                 \nID Options: {id_options}
                                 \rBook ID: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
                the_book = session.query(Book).filter(Book.id==id_choice).first()
                print(f'''
                       \n{the_book.title} by {the_book.author}
                       \rPublished: {the_book.published_date}
                       \rPrice: ${the_book.price / 100}
                       ''')
                submenu_choice = submenu()
                if submenu_choice == '1':
                    the_book.title = edit_check('Title', the_book.title)
                    the_book.author = edit_check('Author', the_book.author)
                    the_book.price = edit_check('Price', the_book.price)
                    the_book.published_date = edit_check('Published', the_book.published_date)
                    session.commit()
                    print('Book Updated!')
                    time.sleep(1)
                elif submenu_choice == '2':
                    session.delete(the_book)
                    session.commit()
                    print('Book Deleted!')
                    time.sleep(1)
        elif choice == '4':
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
            print(f'''
                  \n******* BOOK ANALYSIS *******
                  \rOldest Book: {oldest_book}
                  \rNewest Book: {newest_book}
                  \rTotal Books: {total_books}
                  \rNumber of Python Books: {python_books}''')
            input('\nPress Enter to return to Main Menu.')
        else:
            print('Goodbye...')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
