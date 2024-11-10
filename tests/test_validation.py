import unittest
from validator import validate_receipt

class TestValidators(unittest.TestCase):
    def test_validate_receipt_valid(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item 1", "price": "1.00"}],
            "total": "1.00"
        }
        try:
            validate_receipt(receipt)
        except ValueError:
            self.fail("validate_receipt() raised ValueError unexpectedly!")

    def test_validate_receipt_missing_field(self):
        receipt = {
            "retailer": "Target",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item 1", "price": "1.00"}],
            "total": "1.00"
        }
        with self.assertRaises(ValueError):
            validate_receipt(receipt)

    # Additional test cases...

if __name__ == '__main__':
    unittest.main()
