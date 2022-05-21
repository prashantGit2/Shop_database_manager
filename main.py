import pymongo

def setup_customer_collection(db):
    cust_col = db["customers"]
    if not is_old_database:
        print("\nWe are going to initialize customers collection: ")
        print("****Entering One row/Document is neccesary!****")
        ENTER_A_ROW(cust_col)
    will_add_row = input("Do you wish to add customers: [y/n]:").lower()
    while will_add_row == 'y':
        ENTER_A_ROW(cust_col)
        will_add_row = input("\nDo you wish to add more customers: [y/n]:").lower()

def setup_products_collection(db):
    prod_col = db["products"]
    if not is_old_database:
        print("\nWe are going to initialize products collection: ")
        print("****Entering One row/Document is neccesary!****")
        ENTER_A_ROW(prod_col)
    will_add_row = input("Do you wish to add products: [y/n]:").lower()
    while will_add_row == 'y':
        ENTER_A_ROW(prod_col)
        will_add_row = input("Do you wish to add more products: [y/n]:").lower()

def get_info(collection):
    for row in collection.find():
        print(row)


def ENTER_A_ROW(collection):
    if collection.name == 'customers': #name and address are neccesary in customer col
        #taking customers' name and address
        customer_name = input("Enter customer name: ")
        customer_address = input("Enter customer address: ")

        #creating a dict to store customer data
        data = {"name":customer_name,"address":customer_address}

    elif collection.name == 'products':
        #taking products, name and price
        product_name = input("Enter product Name: ")
        product_price = int(input("Enter product Price: "))

        data = {"name":product_name, "price":product_price}

    #if you wish to add more fields
    will_add_field = input("Do you wish to add more fields: [y/n]: ").lower()
    while will_add_field == 'y':

        field_name = input("Enter field name: ")
        field_data = input("Enter field data: ")

        data[field_name] = field_data

        will_add_field = input("Do you wish to add more fields: [y/n]: ").lower()
    collection.insert_one(data)
def view_data(db):
        is_view_data = input("Do you wish to view data [y/n]:").lower()
        if is_view_data == 'y':
            query_id = int(input("Enter 1 to view customers data\nEnter 2 to view products data\nEnter -1 to quit: "))
            if query_id == 1:
                collection = db["customers"]
                get_info(collection)
            elif query_id == 2:
                collection = db["products"]
                get_info(collection)
            elif query_id == -1:
                quit()
            else:
                print("invalid response!\please try again!:")
                view_data()
def delete_row(db):
    n = int(input("Enter accordingly which collection record you wish to delete\nproducts => 1\ncustomers => 2\n:"))
    if n == 1:
        col = db["products"]
    elif n== 2:
        col = db["customers"]    
    query_name = input("Enter the field name of the document you wish to delete: ")
    query_data = input("Enter the data of the field name you wish to delete: ")
    query = {query_name:query_data}
    col.delete_one(query)


def main():
    #greeting
    print("****Welcome to Shop Database manager****")
    if is_old_database:
        print("Welcome back")
    else:
        print("****We will setup your shop database****")

    setup_customer_collection(mydb)
    setup_products_collection(mydb)

    view_data(mydb)
    
    do_delete_a_row = True if input("Do you wish to delete a record [y/n]: ") == 'y' else False
    while do_delete_a_row:
        delete_row(mydb)
        do_delete_a_row = True if input("Do you wish to delete a record [y/n]: ") == 'y' else False
        
        
    

if __name__ == "__main__":
    #connecting to Mongo client with pymongo and initializing database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    shop_name = input("What is the name of your shop?: ")
    mydb = myclient[shop_name]

    is_old_database = True if shop_name in myclient.list_database_names() else False
    main()
