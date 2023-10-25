import csv
import xml.etree.ElementTree as ET
import sqlite3
from xmlrpc.server import SimpleXMLRPCServer

server = SimpleXMLRPCServer(('localhost', 12345))
server.register_introspection_functions()

def read_csv(file_csv):
    print(f"\nReading the data from file '{file_csv}'")

    with open(file_csv, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    return data

def csv_xml(data, file_csv, file_xml):
    print(f"\nConverting the data from file '{file_csv}' to file '{file_xml}'")

    root = ET.Element('data')
    for row in data:
        item = ET.SubElement(root, 'item')
        for key, value in row.items():
            ET.SubElement(item, key).text = value

    xml_tree = ET.ElementTree(root)
    xml_tree.write(file_xml)

def xml_sql(file_xml, file_db):
    print(f"\nCreating database table")

    db_connection = sqlite3.connect(file_db)
    db_cursor = db_connection.cursor()

    create_table_query = '''CREATE TABLE IF NOT EXISTS car_data (uid INTEGER, car_vin TEXT, car_company TEXT, car_model TEXT, car_model_year TEXT, car_color TEXT)'''
    db_cursor.execute(create_table_query)

    tree = ET.parse(file_xml)
    root = tree.getroot()

    print(f"\nInserting the data from file '{file_xml}' to database table 'car_data'")

    check_query = "SELECT COUNT(*) FROM car_data WHERE uid = ? AND car_vin = ? AND car_company = ? AND car_model = ? AND car_model_year = ? AND car_color = ?"

    for item in root.findall('item'):
        uid = item.find('uid').text
        car_vin = item.find('car_vin').text
        car_company = item.find('car_company').text
        car_model = item.find('car_model').text
        car_model_year = item.find('car_model_year').text
        car_color = item.find('car_color').text

        db_cursor.execute(check_query, (uid, car_vin, car_company, car_model, car_model_year, car_color))
        exists = db_cursor.fetchone()[0]

        if exists == 0:
            insert_query = "INSERT INTO car_data (uid, car_vin, car_company, car_model, car_model_year, car_color) VALUES (?, ?, ?, ?, ?, ?)"
            values = (uid, car_vin, car_company, car_model, car_model_year, car_color)
            db_cursor.execute(insert_query, values)

    db_connection.commit()
    db_cursor.close()
    db_connection.close()

    print("\nData has been sucessfully inserted into table data")

def format_data(results):
    formatted_results = []
    
    for row in results:
        formatted_row = f"'ID': {row[0]}\n'VIN': {row[1]}\n'Company': {row[2]} - 'Model': {row[3]}\n'Year': {row[4]} - 'Color': {row[5]}\n"
        formatted_results.append(formatted_row)
    
    return formatted_results

# Funções para seleção na base de dados
def select_company(company_name):
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM car_data WHERE car_company LIKE ?", ('%' + company_name + '%',))
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    formatted_results = format_data(results)
    return formatted_results

def select_model(model_name):
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM car_data WHERE car_model LIKE ?", ('%' + model_name + '%',))
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    formatted_results = format_data(results)
    return formatted_results

def select_all():
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM car_data")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    formatted_results = format_data(results)
    return formatted_results

def select_color(color):
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM car_data WHERE car_color LIKE ?", ('%' + color + '%',))
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    formatted_results = format_data(results)
    return formatted_results

# Registrar funções de seleção no servidor RPC
server.register_function(select_company)
server.register_function(select_model)
server.register_function(select_all)
server.register_function(select_color)

def main():
    try:
        print("\n-----------------------> CAR DATA PARSING SERVER <-----------------------")

        file_csv = 'car_data.csv'
        file_xml = 'car_data.xml'
        file_db = 'database.db'
    
        data = read_csv(file_csv)
        csv_xml(data, file_csv, file_xml)
        xml_sql(file_xml, file_db)
        print("\n--------------> RPC SERVER CONNECTION HAS BEEN INITIALIZED <--------------")
        server.serve_forever()
    except KeyboardInterrupt:
        print("------------------>RPC SERVER CONNECTION HAS BEEN SHUTDOWN<-----------------")

if __name__ == "__main__":
    main()
