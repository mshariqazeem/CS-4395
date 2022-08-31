import sys
import re
import pickle


# Create a Person class
class Person:
    # Constructor
    def __init__(self, last, first, mi, pid, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.pid = pid
        self.phone = phone

    # Display information about the person calling the method
    def display(self):
        print('Employee Id: ', self.pid)
        print('\t\t\t ', self.first, ' ', self.mi, ' ', self.last)
        print('\t\t\t ', self.phone)


# Function to process the file data
def process_file(persons):
    # Check if the file path has been specified in the sys.arg
    if len(sys.argv) <= 1:
        print('Error: File path not specified')
    else:
        # Open file for reading
        input_file = open(str(sys.argv[1]), 'r')
        # Avoid the header line
        input_file.readline()
        # Read line by line
        while True:
            line = input_file.readline().strip()
            # Check for the end of the line
            if not line:
                break
            # Split line into separate tokens
            tokens = line.split(',')
            # Capitalize the first letter of the first and last name
            tokens[0] = tokens[0].capitalize()
            tokens[1] = tokens[1].capitalize()
            # Check if the middle initial is provided; Assign 'X' if not
            if len(tokens[2]) != 1:
                tokens[2] = 'X'
            # Validate the ID's pattern and check for duplicate key
            while (re.match("[A-Za-z]{2}[0-9]{4}", tokens[3]) is None) or (tokens[3] in persons):
                if tokens[3] in persons:
                    print('ID already exists: ', tokens[3])
                    tokens[3] = input('Please enter a different ID: ')
                else:
                    print('ID invalid: ', tokens[3])
                    print('ID is two letters followed by 4 digits')
                    tokens[3] = input('Please enter a valid ID: ')
            # Validate the phone number's pattern
            while re.match('[0-9]{3}-[0-9]{3}-[0-9]{4}', tokens[4]) is None:
                print('Phone ', tokens[4], ' is invalid')
                print('Enter phone number in form 123-456-7890')
                tokens[4] = input('Enter phone number: ')
            # Create a Person object based on the valid values
            person = Person(tokens[0], tokens[1], tokens[2].capitalize(), tokens[3], tokens[4])
            # Add the Person object into the Persons dictionary
            persons[tokens[3]] = person
        input_file.close()


# Main function
def main():
    # Create a Person dictionary
    persons = {}
    # Populate the dictionary
    process_file(persons)
    # Save the dictionary as a pickle file
    pickle.dump(persons, open('dict.p', 'wb'))  # write binary
    # Unpickle the dictionary from the pickle file
    dict_in = pickle.load(open('dict.p', 'rb'))  # read binary
    # display each person from the persons dictionary
    print('\nEmployee list:')
    for p in dict_in:
        persons[p].display()


# Start here
main()
