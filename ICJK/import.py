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

    # Get cars
    Car_ID = row['Car_ID']
    Car_MakeName = row['Car_MakeName']
    Car_Model = row['Car_Model']
    Car_Series = row['Car_Series']
    Car_SeriesYear = row['Car_SeriesYear'].replace('NULL', '0')
    Car_PriceNew = row['Car_PriceNew'].replace('NULL', '0')
    Car_EngineSize = row['Car_EngineSize'].replace('NULL', '0.0').replace('L','')
    Car_FuelSystem = row['Car_FuelSystem']
    Car_TankCapacity = row['Car_TankCapacity'].replace('NULL', '0').replace('L','')
    Car_Power = row['Car_Power'].replace('NULL', '0').replace('Kw','')
    Car_SeatingCapacity = row['Car_SeatingCapacity'].replace('NULL', '0')
    Car_StandardTransmission = row['Car_StandardTransmission']
    Car_BodyType = row['Car_BodyType']
    Car_Drive = row['Car_Drive']
    Car_Wheelbase = row['Car_Wheelbase'].replace('NULL', '0').replace('mm','')
    
    carsData.add(tuple([Car_ID,Car_MakeName,Car_Model,Car_Series,Car_SeriesYear,Car_PriceNew,
                     Car_EngineSize,Car_FuelSystem,Car_TankCapacity,Car_Power,Car_SeatingCapacity,
                     Car_StandardTransmission,Car_BodyType,Car_Drive,Car_Wheelbase]))

    # Get Orders
    Order_ID = row['\ufeffOrder_ID']
    Order_CreateDate = row['Order_CreateDate'].strip()
    Order_CreateDate = datetime.datetime.strptime(Order_CreateDate, "%Y%m%d").strftime("%Y-%m-%d")
    Order_PickupDate = row['Order_PickupDate'].strip()
    Order_PickupDate = datetime.datetime.strptime(Order_PickupDate, "%Y%m%d").strftime("%Y-%m-%d")
    Order_ReturnDate = row['Order_ReturnDate'].strip()
    Order_ReturnDate = datetime.datetime.strptime(Order_ReturnDate, "%Y%m%d").strftime("%Y-%m-%d")
    fk_car_id = int(row['Car_ID'])
    fk_customer_id = int(row['Customer_ID'])
    fk_pickup_store_id = int(row['Order_PickupStore'])
    fk_return_store_id = int(row['Order_ReturnStore'])
    
    orderData.add(tuple([Order_ID,Order_CreateDate,Order_PickupDate,Order_ReturnDate,
                     fk_car_id,fk_customer_id,fk_pickup_store_id,fk_return_store_id]))

for row in storeData:
    s = Store(id=row[0], name=row[1], address=row[2], phone=row[3], city=row[4], state=row[5])
    s.save()

for row in customerData:
    c = Customer(id=row[0], name=row[1], address=row[2], phone=row[3], birthday=row[4], occupation=row[5], gender=row[6])
    c.save()   
    c = Customer(id=row[0], name=row[1], address=row[2], phone=row[3], birthday=row[4], 
        occupation=row[5], gender=row[6])
    c.save()   

for row in carsData:
    cars = Car(id=row[0], make_name=row[1], model=row[2],series=row[3],series_year=row[4],
        price_new=row[5], engine_size=row[6], fuel_system=row[7], tank_capacity=row[8], 
        power=row[9], seating_capacity=row[10], standard_transmission=row[11], body_type=row[12],
        drive=row[13], wheelbase=row[14])
    cars.save()

