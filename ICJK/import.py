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

    # Get customers
    Customer_ID = row['Customer_ID']
    Customer_Name = row['Customer_Name']
    Customer_Phone = row['Customer_Phone'].replace('1 (11)', '').replace('-','') \
        .replace(' ','').replace('NULL','0').replace('*','')
    Customer_Addresss = row['Customer_Addresss']
    Customer_Brithday = row['Customer_Brithday'].strip()  
    Customer_Brithday = datetime.datetime.strptime(Customer_Brithday, "%d/%m/%Y").strftime("%Y-%m-%d")
    Customer_Occupation = row['Customer_Occupation']
    Customer_Gender = row['Customer_Gender']
    
    customerData.add(tuple([Customer_ID,Customer_Name,Customer_Addresss,Customer_Phone,
                     Customer_Brithday,Customer_Occupation,Customer_Gender]))

for row in storeData:
    s = Store(id=row[0], name=row[1], address=row[2], phone=row[3], city=row[4], state=row[5])
    s.save()

for row in customerData:
    c = Customer(id=row[0], name=row[1], address=row[2], phone=row[3], birthday=row[4], occupation=row[5], gender=row[6])
    c.save()   
