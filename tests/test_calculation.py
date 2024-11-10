import unittest
from calculator import calculate_points
from datetime import datetime, time

class TestCalculatePoints(unittest.TestCase):
    def test_calculate_points_example1(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": datetime.strptime("2022-01-01", "%Y-%m-%d"),
            "purchaseTime": datetime.strptime("13:01", "%H:%M").time(),
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
            ],
            "total": "35.35"
        }
        expected_points = 28  # Based on the example
        actual_points = calculate_points(receipt)
        self.assertEqual(actual_points, expected_points)

    # Additional test cases...

if __name__ == '__main__':
    unittest.main()
