from datetime import datetime

def validate_receipt(receipt):
    """
    Validates the receipt data to ensure all required fields are present and correctly formatted.
    Raises ValueError if validation fails.
    """
    required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for field in required_fields:
        if field not in receipt:
            raise ValueError(f"Missing required field: {field}")
    
    # retailer
    if not isinstance(receipt['retailer'], str) or not receipt['retailer'].strip():
        raise ValueError("Retailer name must be a non-empty string")
    
    # purchaseDate
    try:
        datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
    except ValueError:
        raise ValueError("purchaseDate must be in 'YYYY-MM-DD' format")
    
    # purchaseTime
    try:
        datetime.strptime(receipt['purchaseTime'], "%H:%M")
    except ValueError:
        raise ValueError("purchaseTime must be in 24hrs format like 'HH:MM', no AM or PM")
    
    # total
    try:
        total = float(receipt['total'])
        if total <= 0:
            raise ValueError("Total must be positive")
        
    except ValueError:
        raise ValueError("Total must be a valid number. ")
    
    # items
    if not isinstance(receipt['items'], list) or not receipt['items']:
        raise ValueError("Items must be a non-empty list.")
    for item in receipt['items']:
        if 'shortDescription' not in item or 'price' not in item:
            raise ValueError("Each item must contain 'shortDescription' and 'price'.")
        if not isinstance(item['shortDescription'], str) or not item['shortDescription'].strip():
            raise ValueError("Item 'shortDescription' must be a non-empty string.")
        try:
            price = float(item['price'])
            if price <= 0:
                raise ValueError("Item 'price' must be a positive number.")
        except ValueError:
            raise ValueError("Item 'price' must be a valid number.")
