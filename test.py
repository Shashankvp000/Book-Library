def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


valid_Object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 1212121212
}

missing_name = {
    'price': 6.99,
    'isbn': 1212121212
}

missing_price = {
    'name': 'F',
    'isbn': 1212121212
}

missing_isbn = {
    'name': 'F',
    'price': 6.99
}

empty_dictionary = {}
