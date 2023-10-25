import xmlrpc.client
import sys
import os

def print_results(results, page, res_page):
    sindex = (page - 1) * res_page
    eindex = sindex + res_page
    p_results = results[sindex:eindex]

    print(f"\n Showing {len(p_results)} results from page {page}:")
    print("--------------------------------------------------------------------------")
    for data in p_results:
        print(data)
    print("--------------------------------------------------------------------------")

def select_company(server):
    while True:
        response = input("\nSearch a car by a car company or type '/return' to quit: ").lower()
        if response == "/return":
            break
        else:
            results = server.select_company(response)
            if not results:
                print(f"\nThere's no cars from company '{response}'\n")
            else:
                print("\n----------------------------------------------")
                print(f"{len(results)} Results from search '{response}'")
                print("----------------------------------------------\n")
                for data in results:
                    print(data)

def select_model(server):
    while True:
        response = input("\nSearch a car by a car model or type '/return' to quit: ").lower()
        if response == "/return":
            break
        else:
            results = server.select_model(response)
            if not results:
                print(f"\nThere's no cars with the model '{response}'\n")
            else:
                print("\n----------------------------------------------")
                print(f"{len(results)} Results from search '{response}'")
                print("----------------------------------------------\n")
                for data in results:
                    print(data)

def select_all(server):
    page = 1
    res_page = 100
    while True:
        results = server.select_all()
        if not results:
            response = input("There's no data on the database. Type '/return' to quit: ").lower()
            if response == "/return":
                break
        if results:
            print_results(results, page, res_page)
            cli_response = input("\nType 'n' to go next page, 'p' for the previous page, or '/return' leave:").lower()
            if cli_response == "n" and (page * res_page) < len(results):
                page += 1
                print_results(results, page, res_page)
            elif cli_response == "p" and page > 1:
                page -= 1
                print_results(results, page, res_page)
            elif cli_response == "/return":
                break
            else:
                print("\nInvalid action. Try again.")

def select_color(server):
    while True:
        response = input("Search a car by color or type '/return' to quit: ").lower()
        if response == "/return":
            break
        else:
            results = server.select_color(response)
            if not results:
                print(f"\nThere's no cars with the color '{response}'\n")
            else:
                print("\n----------------------------------------------")
                print(f"{len(results)} Results from search '{response}'")
                print("----------------------------------------------\n")
                for data in results:
                    print(data)


def main():
    server = xmlrpc.client.ServerProxy('http://localhost:12345')

    while True:
        os.system("cls")
        print("\n --------> Menu <---------")
        print("1 - Select by car manufacturer")
        print("2 - Select by car models")
        print("3 - Select all cars")
        print("4 - Select by color")
        print("0 - Leave program")
        option = input("Choose an option: ")
        os.system("cls")

        if option == '1':
            select_company(server)
        elif option == '2':
            select_model(server)
        elif option == '3':
            select_all(server)
        elif option == '4':
            select_color(server)
        elif option == '0':
            sys.exit(1)
        else:
            print("\nInvalid Option, Try Again.")

if __name__ == "__main__":
    main()