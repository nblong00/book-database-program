from models import (Base, session,
                    Book, engine)


# import models
# main menu - add, search, analysis, view
# add books to db
# edit books
# delete books
# search books
# data cleaning
# loop that runs program


if __name__ == '__main__':
    Base.metadata.create_all(engine)