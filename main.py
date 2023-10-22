import csv
import xml.etree.ElementTree as ET
import sqlite3

csv_filename = 'car_data.csv'
xml_filename = 'car_data.xml'

print("\n------------> CAR DATA PARSING XML FILE <------------")

print(f"\nReading the data from file '{csv_filename}'")

with open(csv_filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = [row for row in csv_reader]

print(f"\nConverting the data from file '{csv_filename}' to file '{xml_filename}'")

root = ET.Element('data')
for row in data:
    item = ET.SubElement(root, 'item')
    for key, value in row.items():
        ET.SubElement(item, key).text = value

xml_tree = ET.ElementTree(root)
xml_tree.write(xml_filename)

db_connection = sqlite3.connect('database.db')
db_cursor = db_connection.cursor()

print(f"\nCreating database table to insert the data")

create_table_query = '''CREATE TABLE IF NOT EXISTS car_data (uid INTEGER, car_vin TEXT, car_company TEXT, car_model TEXT, car_model_year TEXT, car_color TEXT)'''
db_cursor.execute(create_table_query)

xml_filename = 'car_data.xml'
tree = ET.parse(xml_filename)
root = tree.getroot()

print(f"\nInserting the data from file '{xml_filename}' to database table 'car_data'")

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

print("\nThe data has been sucessfully inserted into table data\n")

