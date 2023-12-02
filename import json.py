import json
from collections import UserDict
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
class Name(Field):
    pass
class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)
    def validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone should be 10 digits')
class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in (phones or [])]
        self.birthday = birthday
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    def find(self, query):
        matching_records = []
        for record in self.data.values():
            if isinstance(record, Record) and query.lower() in record.name.value.lower():
                matching_records.append(record)
            for phone in record.phones:
                if isinstance(phone, Phone) and query in phone.value:
                    matching_records.append(record)
                    break  # Avoid duplication of records
        return matching_records
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            return f"Contact with name {name} not found"
    def iterator(self, batch_size=10):
        keys = list(self.data.keys())
        for i in range(0, len(keys), batch_size):
            yield [self.data[key] for key in keys[i:i + batch_size]]
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            data = {key: value.__dict__ for key, value in self.data.items() if isinstance(value, Record)}
            json.dump(data, file)
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.data = {key: Record(**value) for key, value in data.items() if isinstance(value, dict)}
        except FileNotFoundError:
            print("File not found. Starting with an empty AddressBook.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Starting with an empty AddressBook.")
def main():
    address_book = AddressBook()
    address_book.load_from_file("address_book.json")  # Відновлення збережених даних
    while True:
        print("\n1. Add Contact")
        print("2. Search Contacts")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter contact name: ")
            birthday = input("Enter birthday (optional, format: YYYY-MM-DD): ")
            record = Record(name, birthday=birthday)
            address_book.add_record(record)
        elif choice == "2":
            query = input("Enter search query (name or phone number): ")
            matching_records = address_book.find(query)
            if matching_records:
                print("\nMatching Contacts:")
                for record in matching_records:
                    print(record)
            else:
                print("No matching contacts found.")
        elif choice == "3":
            address_book.save_to_file("address_book.json")  # Збереження даних перед виходом
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
if __name__ == "__main__":
    main()

