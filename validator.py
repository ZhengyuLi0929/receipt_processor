from datetime import datetime, date
import re
import logging
from decimal import Decimal, InvalidOperation

# regex patterns to match the requirements
RETAILER_PATTERN = re.compile(r"^[\w\s\-&]+$")
SHORT_DESCRIPTION_PATTERN = re.compile(r"^[\w\s\-]+$")
PRICE_PATTERN = re.compile(r"^\d+\.\d{2}$")

# field required for receipt and item
required_fields = {'retailer', 'purchaseDate', 'purchaseTime', 'items', 'total'}
required_items_field = {'shortDescription', 'price'}

def validate_receipt(receipt):
    """
    Validates the receipt data to ensure all required fields are present and correctly formatted.
    Raises ValueError if validation fails.
    """
    # general
    unexpected_fields = set(receipt.keys()) - required_fields
    if unexpected_fields:
        raise ValueError(f"Unexpected fields in receipt: {unexpected_fields}")

    for field in required_fields:
        if field not in receipt:
            raise ValueError(f"Missing required field: {field}")
    
    # retailer
    if not isinstance(receipt['retailer'], str) or not receipt['retailer'].strip():
        raise ValueError("Retailer name must be a non-empty string")
    if not RETAILER_PATTERN.match(receipt['retailer']):
        raise ValueError("Retailer must be a non-empty string containing only alphanumeric characters, spaces, hyphens, and ampersands")
    
    # purchaseDate
    if not isinstance(receipt['purchaseDate'], str):
        raise ValueError("purchaseDate must be passed as a string")
    try:
        purchase_date = receipt['purchaseDate'].strip()        
        parsed_date = datetime.strptime(purchase_date,  "%Y-%m-%d").date()
        if parsed_date > date.today():
            raise ValueError("purchaseDate cannot be in the future")
    except ValueError:
        raise ValueError("purchaseDate must be in 'YYYY-MM-DD' format and cannot be in the future")
    
    # purchaseTime
    if not isinstance(receipt['purchaseTime'], str):
        raise ValueError("purchaseDate must be passed as a string")
    try:
        parsed_time = datetime.strptime(receipt['purchaseTime'], "%H:%M").time()
    except ValueError:
        raise ValueError("purchaseTime must be in 24hrs format like 'HH:MM', no AM or PM")
    
    # datetime can't be in the future
    combined_datetime = datetime.combine(parsed_date, parsed_time)
    if combined_datetime > datetime.now():
        logging.info("Processed datetime: %s, Current datetime: %s", combined_datetime, datetime.now())
        raise ValueError("The combined purchaseDate and purchaseTime cannot be in the future")
    
    # total
    total = receipt['total']
    if not isinstance(total, str):
        raise ValueError("Total in JSON must be passed as a string")
    if not PRICE_PATTERN.match(total):
        raise ValueError("Total must be a valid positive number, no comma, with exactly two decimal places.")
    
    # items
    if not isinstance(receipt['items'], list) or not receipt['items']:
        raise ValueError("Items must be a non-empty list.")
    
    calculated_total = 0
    total_decimal = Decimal(total)
    for item in receipt['items']:
        # general
        unexpected_item_fields = set(item.keys()) - required_items_field
        if unexpected_item_fields:
            raise ValueError(f"Unexpected fields in item: {unexpected_item_fields}")
        
        # short description
        if 'shortDescription' not in item or 'price' not in item:
            raise ValueError("Each item must contain 'shortDescription' and 'price'.")
        if not isinstance(item['shortDescription'], str) or not item['shortDescription'].strip():
            raise ValueError("Item 'shortDescription' must be a non-empty string.")
        if not SHORT_DESCRIPTION_PATTERN.match(item['shortDescription']):
            raise ValueError("Item 'shortDescription' must be a string containing only alphanumeric characters, spaces, and hyphens.")
        
        # price
        price = item['price']
        if not isinstance(price, str):
            raise ValueError("Item price in JSON must be passed as a string")
        if not PRICE_PATTERN.match(price):
            raise ValueError("Item 'price' must be a valid positive number, no comma, with exactly two decimal places.")
        calculated_total += Decimal(price)

    if total_decimal != calculated_total:
        raise ValueError(f"The total amount '{total}' does not match the sum of item prices '{calculated_total}'.")
    
        