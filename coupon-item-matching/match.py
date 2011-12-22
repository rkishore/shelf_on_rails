
import sys

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
    free_returns_dollar_qualifier, fixed_return_rate, standard_return_rate

    # Expires
    expiration_date
    
    # Availability
    In Stores only, Online only, Both'''
    
    
#coupon1 = {"store": "JCrew", "discount": "0.3", 
#              "category": "1", "FREE_SHIPPING": "1", "QUALIFIER": "50", "CODE": "SNOWMAN"}

INFINITY = 10000
coupon_jcrew = {"store": "JCrew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "CODE1",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "CODE2",
                "item_cat": "MENS-SHIRT", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": 100, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_jcrew_dec_22 = {"store": "JCrew", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 175, "discount_shipping_rate": "None", "standard_shipping_rate": 8.95,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }
               
coupon_jcrew_dec_18 = {"store": "JCrew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "-",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_22 = {"store": "Express", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "-",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }


coupon_abercrombie_dec_22 = {"store": "ABERCROMBIE", 
                "stw_discount": 0.4, "stw_discount_perc_code": "15399",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_banana_dec_22 = {"store": "BANANA_REPUBLIC", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.3, "add_stw_discount_perc_code": "BRWINTER",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_aerie_dec_22 = {"store": "AERIE", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.4, "add_stw_discount_perc_code": "39427841",
                "item_cat": "-", "buy1_get1_discount_perc": 0.25, "buy1_get1_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

# Item = ["store name", "category", "price", "sale price"]
# Men
item1 = {"store": "JCrew", "category": "MENS-SHIRT", "price": 49.99, "sale_price": 49.99}
# Women
item2 = {"store": "JCrew", "category": "PANT", "price": 59.99, "sale_price": 39.99}

DEFAULT_SHIPPING_COST = 10 # Placeholder: Need to dynamically determine shipping cost    

def aggregate_discount_check(coupon, total_price):
    
    if coupon["stw_discount_dollars"] > 0:
        if total_price > coupon["stw_discount_dollars_lower_bound"]:
            total_price -= coupon["stw_discount_dollars"]
            print "DBG: total price reduced to " + str(total_price)
        else:
            print "DBG: Sorry. Buy for " + str(coupon["stw_discount_dollars_lower_bound"]-total_price) + "to get additional " + str(coupon["stw_discount_dollars"]) + " discount!" 
    else:
        print "DBG: Sorry. No $X with $Y style discounts right now"

    return total_price
            

def check_shipping(coupon, total_price):
    if (total_price >= coupon["free_shipping_dollar_qualifier"]):
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
    print "DBG: Discount: " + str(disc) + " Base price " + str(price) + " Sale price: " + str(res)
    return res

def match(coupon, item):
    # iterate over all items
    # same store
    if item["store"] == coupon["store"]:
        
        # First check store-wide discounts
        if coupon["stw_discount"] > 0: # and coupon["stw_discount_flag"] == 0:
            item["sale_price"] = apply_discount(coupon["stw_discount"], item["price"])
            
            if coupon["add_stw_discount"] > 0:  # and coupon["add_stw_discount_flag"] == 0:
                item["sale_price"] = apply_discount(coupon["add_stw_discount"], item["sale_price"])
          
        # same category
        if (category_match(coupon["item_cat"], item["category"])):
            item["sale_price"] = apply_discount(coupon["buy1_get1_discount_perc"], item["sale_price"])
                    
    return True

def read_item_info(filename):
    print "Processing " + filename
    f = open(filename, 'r')
    itemlist = []
    i = 0
    for line in f:
        itemdata_arr = line.split("|")
        price_arr = itemdata_arr[2].split(",")
        #if itemdata_arr[1].strip() == "mens-shirts":
            #print itemdata_arr[0].strip(), itemdata_arr[1].strip(), price_arr[0].strip(), price_arr[1].strip()
        itemlist.append( {"store": itemdata_arr[0].strip(), 
                          "category": itemdata_arr[1].strip(), 
                          "price": float(price_arr[0].strip()),
                          "sale_price": float(price_arr[1].strip())} )
        i += 1

    #print len(itemlist)        
    return itemlist

        

if __name__ == "__main__":
    
    print "Number of input item files: " + str(len(sys.argv)-1)

    store_itemlist = []
    for i in range(1,len(sys.argv)):
        store_itemlist.append(read_item_info(sys.argv[i]))

    print store_itemlist[0][0]
    print store_itemlist[1][0]
    
    base = base_price(item1, item2)

    match(coupon_jcrew, item1)
    match(coupon_jcrew, item2)

    total_price = float(item1["sale_price"]) + float(item2["sale_price"])
    print "DBG: Total item price: " + str(total_price)

    aggregate_discount_check(coupon_jcrew, total_price)
    shipping_cost = check_shipping(coupon_jcrew, total_price)
    total_price += shipping_cost

    print "Base cost: " + str(base) + " Discounted cost: " + str(total_price) + " Savings: " + str(base-total_price)
    
