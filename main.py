import pickle
from address_book import AddressBook, Record

debug = True

def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except Exception as exception:
            print(f"[INPUT_ERROR] {exception}")
            return ""
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args, book):
    name, date, *_ = args
    record = book.find(name)
    message = f"Contact '{name}' successfully get birthday date: {date}."
    if record:
        record.add_birthday(date)
    else:
        message = f"Contact '{name}' not in the list"
    return message

@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record:
        return record.show_birthday()
    else:
        return f"Contact '{name}' not in the list"

#@input_error
def birthdays(args, book):
    days = None
    if args:
        days, = args
        return book.get_upcoming_birthdays(days)
    else:
        return book.get_upcoming_birthdays()


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error   
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = f"Contact '{name}' successfully changed {old_phone} = {new_phone}."
    if record:
        record.edit_phone(old_phone, new_phone)
    else:
        message = f"Contact '{name}' not in the list"
    return message

    
@input_error
def show_phone(args, book):
    name, = args
    record = book.find(name)
    if record:
        return record.show_phones()
    else:
        return f"Contact '{name}' not in the list"


@input_error    
def show_all(args, book):
    if not args:
        return book
    else:
        raise Exception("Function 'all' don't receive any arguments")

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            continue
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))
            pass

        else:
            print("Invalid command.")
    save_data(book)
            
if __name__ == "__main__":
    main()