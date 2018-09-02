# This will seed the data base with data from data.csv
# need to copy and paste this in to the shell
# python3 manage.py shell

from Home.models import Store, Customer, Car, Order
import csv
import datetime

def clear_database(Order, Store, Customer, Car):
    Order.objects.all().delete()
    Store.objects.all().delete()
    Customer.objects.all().delete()
    Car.objects.all().delete()
    
clear_database(Order, Store, Customer, Car)

storeData = set()
customerData = set()
data = csv.DictReader(open('data.csv'))

for row in data:
    # Get pickup store locations
    Store_ID = row['Order_PickupStore']
    Pickup_Store_Name = row['Pickup_Store_Name'].split('_')[0]
    Pickup_Store_Address = row['Pickup_Store_Address']
    Pickup_Store_Phone = row['Pickup_Store_Phone'].replace('1 (11)', '').replace('-','') \
        .replace(' ','').replace('NULL','0')
    Pickup_Store_City = row['Pickup_Store_City'].strip()
    Pickup_Store_State_Name = row['Pickup_Store_State_Name']
    
    storeData.add(tuple([Store_ID,Pickup_Store_Name,Pickup_Store_Address,Pickup_Store_Phone,
                     Pickup_Store_City,Pickup_Store_State_Name]))
    
    # Get return store locations
    Store_ID = row['Order_ReturnStore']
    Pickup_Store_Name = row['Return_Store_Name'].split('_')[0]
    Pickup_Store_Address = row['Return_Store_Address']
    Pickup_Store_Phone = row['Return_Store_Phone'].replace('1 (11)', '').replace('-','') \
        .replace(' ','').replace('NULL','0')
    Pickup_Store_City = row['Return_Store_City'].strip()
    Pickup_Store_State_Name = row['Return_Store_State']
    
    storeData.add(tuple([Store_ID,Pickup_Store_Name,Pickup_Store_Address,Pickup_Store_Phone,
                     Pickup_Store_City,Pickup_Store_State_Name]))

