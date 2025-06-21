import datetime

def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try: 
        month = months.index(split_date[0]) + 1
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError: 
        input('''
              \n******DATE ERROR******
              \rThe date format should contain a valid Month Day Year.
              \rEx. January 30, 2023
              \rPress Enter to try again.
              \r*********************
            ''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
        return_price = int(price_float * 100)
    except ValueError:
        input('''
              \n******PRICE ERROR******
              \rThe price should be a number without currency symbol.
              \rEx. 29.99
              \rPress Enter to try again.
              \r*********************
            ''')
        return
    else:
        return return_price