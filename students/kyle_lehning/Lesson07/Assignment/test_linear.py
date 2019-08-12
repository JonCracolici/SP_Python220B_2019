#!/usr/bin/env python3
"""
Tests for linear.py
"""
from unittest import TestCase
from unittest.mock import patch
from Assignment import linear

TEST_DB_NAMES = ['test_products', 'test_customers', 'test_rentals']


def clear_test_collections():
    """Clears the collections used for testing"""
    with linear.MONGO:
        db = linear.MONGO.connection.media  # pylint: disable=C0103
        db[TEST_DB_NAMES[0]].drop()
        db[TEST_DB_NAMES[1]].drop()
        db[TEST_DB_NAMES[2]].drop()


class DatabaseUnitTest(TestCase):
    """
    Class for unit tests for linear.py
    """
    def test_import_data(self):
        """
        Test that import_data imports csv into database
        """
        clear_test_collections()
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            incorrect_names = linear.import_data('', 'Products .csv', 'Customers .csv',
                                                 'Rentals .csv')
        return_without_time = [x[:-1] for x in incorrect_names]
        self.assertEqual([(0, 0, 0), (0, 0, 0), (0, 0, 0)], return_without_time)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            import_data = linear.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        import_return_without_time = [x[:-1] for x in import_data]
        self.assertEqual([(1000, 0, 1000), (1000, 0, 1000), (1000, 0, 1000)],
                         import_return_without_time)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            duplicate_data = linear.import_data('', 'Products.csv', 'Customers.csv',
                                                'Rentals.csv')
        duplicate_return_without_time = [x[:-1] for x in duplicate_data]
        self.assertEqual([(1000, 1000, 2000), (1000, 1000, 2000), (1000, 1000, 2000)],
                         duplicate_return_without_time)
        clear_test_collections()
