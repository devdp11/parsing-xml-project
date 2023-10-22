import sqlite3
import os

def select_company(cursor):
    try:
        while True:
            response = input("Search a car by a car company or type '/return' to quit: ")
            if response == "/return".lower():
                os.system("cls")
                break
            else:
                cursor.execute("SELECT * FROM car_data WHERE LOWER(car_company) LIKE ?", ('%' + response.lower() + '%',))
                results = cursor.fetchall()
                if len(results) == 0:
                    print(f"\nThere's no cars from company '{response}'\n")
                else:
                    print(f"\nResults from search '{response}'\n")
                    for data in results:
                        print(data)
    except sqlite3.OperationalError as e:
        os.system("cls")
        print(f"\nAn error has occured: {e}\n")

def select_model(cursor):
    try:
        while True:
            response = input("\nSearch a car by a car model or type '/return' to quit: ")
            if response == "/return":
                    os.system("cls")
                    break
            else: 
                cursor.execute("SELECT * FROM car_data WHERE LOWER(car_model) LIKE ?", ('%' + response.lower() + '%',))
                results = cursor.fetchall()
                if len(results) == 0:
                    print(f"\nThere's no cars with the model '{response}'\n")
                else:
                    print(f"\nResults from search '{response}'\n")
                    for data in results:
                        print(data)
    except sqlite3.OperationalError as e:
        os.system("cls")
        print(f"\nAn error has occured: {e}\n")

def select_all(cursor):
    try:
        while True:
            cursor.execute("SELECT * FROM car_data")
            results = cursor.fetchall()
            if len(results) == 0:
                print("Theres no data on database")
            else:
                print(f"Results from search\n")
                for data in results:
                    print(data)
            
            response = input("\nType '/return' to leave: ")
            if response == "/return":
                os.system("cls")
                break
            else:
                continue
    except sqlite3.OperationalError as e:
        print(f"\nAn error has occured: {e}\n")

def select_color(cursor):
    try:
        while True:
            response = input("Search a car by color or type '/return' to quit: ")
            if response == "/return":
                    os.system("cls")
                    break
            else: 
                cursor.execute("SELECT * FROM car_data WHERE LOWER(car_color) LIKE ?", ('%' + response.lower() + '%',))
                results = cursor.fetchall()
                if len(results) == 0:
                    print(f"\nThere's no cars with the color '{response}'\n")
                else:
                    print(f"\nResults from search '{response}'\n")
                    for data in results:
                        print(data)
    except sqlite3.OperationalError as e:
        os.system("cls")
        print(f"\nAn error has occured: {e}\n")

def main():
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()

    while True:
        print(" --------> Menu <---------")
        print("1 - Select by car companies")
        print("2 - Select by  car models")
        print("3 - Select all cars")
        print("4 - Select by color")
        print("0 - Leave program")

        option = input("Choose an option: ")
        print()

        if option == '1':
            os.system("cls")
            select_company(cursor)
        elif option == '2':
            os.system("cls")
            select_model(cursor)
        elif option == '3':
            os.system("cls")
            select_all(cursor)
        elif option == '4':
            os.system("cls")
            select_color(cursor)
        elif option == '0':
            os.system("cls")
            leave = input("Are you sure you want to leave the program? (y/n):")
            if leave == "y":
                os.system("cls")
                break
            else:
                os.system("cls")
                continue
        else:
            print("Invalid Option, Try Again.")

    cursor.close()
    db_connection.close()

def clear():
    os.system("cls")
    main()

if __name__ == "__main__":
    clear()
