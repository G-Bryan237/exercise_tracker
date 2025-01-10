# Exercise Tracking App

# Define a list to store exercise records
exercise_records = []

# Function to add an exercise record
def add_exercise():
    exercise_type = input("Enter exercise type (e.g., Running, Cycling): ")
    duration = input("Enter duration (e.g., 30 minutes): ")
    date = input("Enter date (e.g., YYYY-MM-DD): ")
    exercise_records.append({"Type": exercise_type, "Duration": duration, "Date": date})
    print("Exercise record added successfully!\n")

# Function to view all exercise records
def view_records():
    if not exercise_records:
        print("No records available.\n")
    else:
        for index, record in enumerate(exercise_records, start=1):
            print(f"{index}. Type: {record['Type']}, Duration: {record['Duration']}, Date: {record['Date']}")
        print()

# Function to edit an exercise record
def edit_record():
    view_records()
    if exercise_records:
        try:
            record_number = int(input("Enter the record number to edit: ")) - 1
            if 0 <= record_number < len(exercise_records):
                exercise_type = input("Enter new exercise type (leave blank to keep current): ")
                duration = input("Enter new duration (leave blank to keep current): ")
                date = input("Enter new date (leave blank to keep current): ")

                if exercise_type:
                    exercise_records[record_number]["Type"] = exercise_type
                if duration:
                    exercise_records[record_number]["Duration"] = duration
                if date:
                    exercise_records[record_number]["Date"] = date

                print("Record updated successfully!\n")
            else:
                print("Invalid record number.\n")
        except ValueError:
            print("Please enter a valid number.\n")

# Function to delete an exercise record
def delete_record():
    view_records()
    if exercise_records:
        try:
            record_number = int(input("Enter the record number to delete: ")) - 1
            if 0 <= record_number < len(exercise_records):
                del exercise_records[record_number]
                print("Record deleted successfully!\n")
            else:
                print("Invalid record number.\n")
        except ValueError:
            print("Please enter a valid number.\n")

# Main menu loop
def main_menu():
    while True:
        print("Exercise Tracking App")
        print("1. Add Exercise Record")
        print("2. View Records")
        print("3. Edit Record")
        print("4. Delete Record")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_exercise()
        elif choice == "2":
            view_records()
        elif choice == "3":
            edit_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Run the main menu
if __name__ == "__main__":
    main_menu()
