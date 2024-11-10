# calculate.py

import re
import math
from datetime import datetime, time
#import logging

def calculate_points(receipt):
    """
    Calculates the total points awarded for the receipt based on the specified rules.
    """
    points = 0
    
    # rule 1: One point for every alphanumeric character in the retailer name
    retailer = receipt['retailer']
    alphanumeric_count = len(re.findall(r'[A-Za-z0-9]', retailer))
    points += alphanumeric_count
    
    # rule 2: 50 points if the total is a round dollar
    total = float(receipt['total'])
    if (total * 100) % 100 == 0:
        points += 50
    
    # rule 3: 25 points if the total is a multiple of 0.25
    if (total * 100) % 25 == 0:
        points += 25
    
    # rule 4: 5 points for every two items
    item_count = len(receipt['items'])
    points += (item_count // 2) * 5
    
    # rule 5: 0.2 points for items with description length a multiple of 3, then round up
    for item in receipt['items']:
        description = item['shortDescription'].strip()
        if len(description) % 3 == 0:
            price = float(item['price'])
            item_points = math.ceil(price * 0.2)
            points += item_points
    
    # rule 6: 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt['purchaseDate'], "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6
    
    # rule 7: 10 points if the time is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt['purchaseTime'], "%H:%M").time()
    start_time = time(14, 0)
    end_time = time(16, 0)  
    if start_time <= purchase_time < end_time:
        points += 10
    
    return points
