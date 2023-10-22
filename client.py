import xmlrpc.client
import sys
import os

def connect_server():
    server = xmlrpc.client.ServerProxy('http://localhost:12345')
    os.system("cls")
    return server

def select_company(server):
    os.system("cls")
    while True:
        response = input("\nSearch a car by a car company or type '/return' to quit: ")
        if response == "/return":
            os.system("cls")
            break
        else:
            results = server.select_company(response)
            if not results:
                os.system("cls")
                print(f"\nThere's no cars from company '{response}'\n")
            else:
                os.system("cls")
                print(f"\nResults from search '{response}'\n")
                for data in results:
                    print(data)

def select_model(server):
    os.system("cls")
    while True:
        response = input("\nSearch a car by a car model or type '/return' to quit: ")
        if response == "/return":
            os.system("cls")
            break
        else:
            results = server.select_model(response)
            if not results:
                os.system("cls")
                print(f"\nThere's no cars with the model '{response}'\n")
            else:
                os.system("cls")
                print(f"\nResults from search '{response}'\n")
                for data in results:
                    print(data)

def select_all(server):
    os.system("cls")
    while True:
        results = server.select_all()
        if not results:
            os.system("cls")
            print("There's no data on database")
        else:
            os.system("cls")
            print(f"Results from search\n")
            for data in results:
                print(data)
            response = input("Type '/return' to quit: ")
            if response == "/return":
                os.system("cls")
                return
            else:
                continue

def select_color(server):
    os.system("cls")
    while True:
        response = input("\nSearch a car by color or type '/return' to quit: ")
        if response == "/return":
            os.system("cls")
            break
        else:
            results = server.select_color(response)
            if not results:
                os.system("cls")
                print(f"\nThere's no cars with the color '{response}'\n")
            else:
                os.system("cls")
                print(f"\nResults from search '{response}'\n")
                for data in results:
                    print(data)

def close_con():
    os.system("cls")
    while True:
        leave = input("Are you sure you want to leave the program? (y/n):")
        if leave == "y":
            os.system("cls")
            sys.exit(0)
        else:
            main()

def main():
    server = connect_server()

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
            select_company(server)
        elif option == '2':
            select_model(server)
        elif option == '3':
            select_all(server)
        elif option == '4':
            select_color(server)
        elif option == '0':
            close_con()
        else:
            print("Invalid Option, Try Again.")

if __name__ == "__main__":
    main()
