"""
Create database for products, customers, and rentals.
"""
import csv
import os
import time
from pymongo import MongoClient


class MongoDBConnection():
    """
    MongoDB Connection
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """
        Init
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Enter
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit
        """
        self.connection.close()


def timer(func):
    """
    Decorator to time functions
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        print('The function {} took {:.5f} seconds to execute.'.format(func.__name__, total_time))
        return result
    return wrapper


@timer
def csv_to_dict(file):
    """
    Creates a list of dictionaries from a csv file
    """
    with open(file) as csv_file:
        key_val_list = []
        for row in csv.DictReader(csv_file):
            temp_dict = {}
            for key, val in row.items():
                temp_dict[key] = val
            key_val_list.append(temp_dict)
    return key_val_list


@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name and three csv files as input, one
    with product data, one with customer data and the third one with rentals
    data and creates and populates a new MongoDB database with these data. It
    returns two tuples the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        products = database['products']
        customers = database['customers']
        rentals = database['rentals']

        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)
        rental_path = os.path.join(directory_name, rentals_file)

        products_err = 0
        customers_err = 0
        rentals_err = 0

        try:
            products.insert_many(csv_to_dict(product_path))
            products_count = len(csv_to_dict(product_path))
        except FileNotFoundError as err:
            products_err += 1
            products_count = 0
        try:
            customers.insert_many(csv_to_dict(customer_path))
            customers_err = 0
            customers_count = len(csv_to_dict(customer_path))
        except FileNotFoundError as err:
            customers_err += 1
            customers_count = 0

        try:
            rentals.insert_many(csv_to_dict(rental_path))
            rentals_err = 0
            rentals_count = len(csv_to_dict(rental_path))
        except FileNotFoundError as err:
            rentals_err += 1
            rentals_count = 0

        added_tuple = (products_count, customers_count, rentals_count)
        error_tuple = (products_err, customers_err, rentals_err)
        return (added_tuple, error_tuple)


@timer
def show_available_products():
    """
    Return a Python dictionary of products listed as
    available with the following fields
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        products = database['products']
        prod_dict = {}
        for prod in products.find():
            if int(prod['quantity_available']):
                prod_dict[prod['product_id']] = {
                    'description': prod['description'],
                    'product_type': prod['product_type'],
                    'quantity_available': prod['quantity_available']
                }
        return prod_dict


@timer
def show_rentals(product_id):
    """
    Return a Python dictionary of products listed as
    available with the following fields
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        rentals = database['rentals']
        customers = database['customers']
        matching_users = []
        user_dict = {}

        for rental in rentals.find():
            if product_id in rental.values():
                matching_users.append(rental['user_id'])

        for cust in customers.find():
            for user in matching_users:
                if user in cust.values():
                    user_dict[cust['user_id']] = {
                        'name': cust['name'],
                        'address': cust['address'],
                        'phone_number': cust['phone_number'],
                        'email': cust['email']
                    }

        return user_dict


@timer
def drop_db():
    """
    Clear the database
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        database.products.drop()
        database.customers.drop()
        database.rentals.drop()


if __name__ == "__main__":
    drop_db()
    print("Timing small csv files: \n")
    import_data('', 'products_short.csv',
                'customers_short.csv',
                'rentals_short.csv')
    show_available_products()
    show_rentals('prd002')
    drop_db()
    print("\n\nTiming long csv files: \n")
    import_data('', 'products_long.csv',
                'customers_long.csv',
                'rentals_long.csv')
    show_available_products()
    show_rentals('prd002')
