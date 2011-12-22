#coupon = ["store name", "% off", "all purchase/category", "free shipping?", "qualifier for shipping", 
#         "code"]
# Categories: 0 => ALL, 1 => MEN, 2 => WOMEN
# Free shipping: 1 => yes, 0 => false
# Qualifier: -1 => ANY, VAL => At least on that much of merchandize
# Code:  

'''class Coupon:
    
    # Store-wide Discounts
    stw_discount_perc, stw_discount_perc_flag, stw_discount_perc_code
    add_stw_discount_perc, add_stw_discount_perc_flag, add_stw_discount_perc_code
    stw_discount_dollars, stw_discount_dollars_flag, stw_discount_dollars_code
    
    # Item-specific
    item_cat buy1_get1_discount_perc, buy1_get1_discount_perc_flag, buy1_get1_discount_perc_code 

    # Shipping 
    free_shipping_dollar_qualifier, fixed_shipping_rate, standard_shipping_rate
    
    # Returns
    free_returns_dollar_qualifier, fixed_return_rate, standard_return_rate'''


#coupon1_stw = {"store": "JCrew", "discount": "0.3", 
#              "category": "1", "FREE_SHIPPING": "1", "QUALIFIER": "50", "CODE": "SNOWMAN"}


coupon1_stw = {"store": "JCrew", 
               "stw_discount": 0.3, "stw_discount_perc_code": "CODE1",
               "add_stw_discount": 0.2, "add_stw_discount_perc_code": "CODE2",
               "item_cat": "MENS-SHIRT", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
               "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
               "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
               "free_returns_dollar_qualifier": 100, "discount_return_rate": "None", "standard_return_rate": 10
               }

               
               
              



# Item = ["store name", "category", "price", "sale price"]
# Men
item1 = {"store": "JCrew", "category": "MENS-SHIRT", "price": 49.99, "sale_price": "None"}
# Women
item2 = {"store": "JCrew", "category": "PANT", "price": 59.99, "sale_price": 39.99}

DEFAULT_SHIPPING_COST = 10 # Placeholder: Need to dynamically determine shipping cost    

def check_shipping(coupon, total_item_cost):
    if (coupon1["FREE_SHIPPING"] == "1"):
        if ( total_item_cost >= float(coupon1["QUALIFIER"]) ):
            print "DBG: Free shipping! Yay!"
            shipping_cost = 0
        else:
            print "DBG: Sorry, no Free Shipping"
            shipping_cost = DEFAULT_SHIPPING_COST         
        return shipping_cost

def base_price(item1, item2):
    shipping_cost = DEFAULT_SHIPPING_COST
    base = float(item1["price"]) + float(item2["price"]) + shipping_cost
    print "DBG: Base total price:" + str(base)
    return base

def category_match(cat1, cat2):
    if cat1 == cat2:
        return True

def apply_discount(disc, price):
    val = float(disc)
    p = float(price)
    res = p - p * val
    print "DBG: Discount: " + disc + " Base price " + price + " Sale price: " + str(res)
    return res

def match(coupon, item):
    # iterate over all items
    # same store
    if item["store"] == coupon["store"]:
        
        # first check the stw
        # same category
        if (category_match(coupon["category"], item["category"])):
            # now check if sale price exists
            if item["sale_price"] == "None":
                item["sale_price"] = apply_discount(coupon["discount"], item["price"])
            else:
                print "DBG: A discount has been already applied, need to check if two coupons can be combined"   
    
    return True


if __name__ == "__main__":
    
    match(coupon1, item1)
    match(coupon1, item2)

    total_price = float(item1["sale_price"]) + float(item2["sale_price"])

    base = base_price(item1, item2)
    print "DBG: Total item price: " + str(total_price)

    shipping_cost = check_shipping(coupon1, total_price)
    total_price += shipping_cost

    print "Base cost: " + str(base) + " Discounted cost: " + str(total_price) + " Savings: " + str(base-total_price)
    