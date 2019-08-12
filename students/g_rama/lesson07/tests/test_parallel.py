"""Testing the database.py"""
import sys
import unittest
import atexit
from line_profiler import LineProfiler
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/'
                'students/g_rama/lesson07/src/')
#pylint: disable=import-error
import parallel
PROFILE = LineProfiler()
atexit.register(PROFILE.print_stats)

DIRECTORY_NAME = "../src/data"


class TestLinear(unittest.TestCase):
    """Test cases for database.py methods"""

    @PROFILE
    def test_import_data(self):
        """Testing of the import data"""
        parallel.drop_collections()
        customer, product = parallel.import_data(DIRECTORY_NAME, "customers.csv",
                                                 "products.csv", "rentals.csv")
        actual_output = customer[0:3], product[0:3]
        expected_output = ((0, 900, 900), (0, 984, 984))
        assert actual_output == expected_output

    # # @profile
    # def test_show_available_products(self):
    #     """Testing the available products function"""
    #     linear.import_data(directory_name, "products.csv", "customers.csv", "rentals.csv")
    #
    #     expected_output = {'p101': {'Electronics', '5', 'TV'},
    #                        'p102': {'Lamp', 'Livingroom', '5'},
    #                        'p103': {'Dining Table', 'Diningroom', '5'},
    #                        'p104': {'5', 'bedroom', 'Queen bed'},
    #                        'p105': {'bedroom', '5', 'Kung bed'},
    #                        'p106': {'studyroom', 'Study Table', '5'},
    #                        'p107': {'kidsroom', 'Bunk Bed', '5'},
    #                        'p108': {'Microwave', 'Electronics', '5'},
    #                        'p109': {'Fan', 'livingroom', '5'},
    #                        'p110': {'5', 'livingroom', 'Heater'}}
    #     actual_data = linear.show_available_products()
    #     linear.drop_collections()
    #     self.assertNotEqual(expected_output, actual_data)
    #
    # # @profile
    # def test_show_rentals(self):
    #     """Function to test the return of user details for a product that is rented"""
    #     linear.import_data(directory_name, "products.csv", "customers.csv", "rentals.csv")
    #     expected_data = {'UID103': {'dom@gmail.com', '3 Seattle Dr', 'Dom'},
    #                      'UID105': {'5 Vincent dr', 'Dan', 'dan@gmail.com'},
    #                      'UID101': {'1 Redmond dr', 'Sam', 'sam@gmail.com'}}
    #     actual_data = linear.show_rentals("p101")
    #     linear.drop_collections()
    #     self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
