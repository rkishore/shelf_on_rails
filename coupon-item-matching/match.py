import sys
import logging
import copy

from operator import itemgetter

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.basicConfig(format='%(message)s', level=logging.INFO)


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
#B1G1 = 1
#CSALE = 2
MENS_SHIRTS= 0
MENS_PANTS= 1
MENS_JEANS= 2
WOMENS_JEANS= 3
WOMENS_SWEATERS= 4

coupon_jcrew = {"store": "J.Crew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "CODE1",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "CODE2",
                "item_cat": "mens-shirts", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": 100, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_jcrew_dec_23 = {"store": "J.Crew", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "item_spec_discount_type": "B1G1","item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 175, "discount_shipping_rate": "None", "standard_shipping_rate": 8.95,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_jcrew_dec_22 = {"store": "J.Crew", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "item_spec_discount_type": "B1G1","item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 175, "discount_shipping_rate": "None", "standard_shipping_rate": 8.95,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }
               
coupon_jcrew_dec_18 = {"store": "J.Crew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "-",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_21 = {"store": "Express", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "-",
                "item_cat": "mens-dress-pants", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_22 = {"store": "Express", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "-",
                "item_cat": "mens-dress-pants", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_23 = {"store": "Express", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "-",
                "item_cat": "mens-dress-pants", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 15, "stw_discount_dollars_lower_bound": 60, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_18 = {"store": "Express", 
                "stw_discount": 0.3, "stw_discount_perc_code": "-",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "mens-dress-pants", "item_spec_discount_type": "B1G1", "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 100, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_abercrombie_dec_18 = {"store": "ABERCROMBIE", 
                "stw_discount": 0.4, "stw_discount_perc_code": "15399",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "outerwear", "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10,
                "where": "in-store"
                }

coupon_abercrombie_dec_22 = {"store": "ABERCROMBIE", 
                "stw_discount": 0.4, "stw_discount_perc_code": "15399",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_abercrombie_dec_23 = {"store": "ABERCROMBIE", 
                "stw_discount": 0.5, "stw_discount_perc_code": "15399",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10,
                "where": "in-store"
                }

coupon_banana_dec_18 = {"store": "BANANA_REPUBLIC", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "BRSALE",
                "item_cat": "women-sweater", "item_spec_discount_perc": 0.4, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }


coupon_banana_dec_22 = {"store": "BANANA_REPUBLIC", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.3, "add_stw_discount_perc_code": "BRWINTER",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_banana_dec_23 = {"store": "BANANA_REPUBLIC", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.3, "add_stw_discount_perc_code": "BRSALE30",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }



coupon_aerie_dec_22 = {"store": "AERIE", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.4, "add_stw_discount_perc_code": "39427841",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

# Item = ["store name", "category", "price", "sale price"]

DEFAULT_SHIPPING_COST = 10 # Placeholder: Need to dynamically determine shipping cost    

def is_not_on_discount(item):
    discount_applied = (item["sale_price"] < item["price"])
    return (not discount_applied)

def calculate_b1g1_discount(store, cat, disc_rate):
    logging.debug("calculate_b1g1_discount: for store " + store + " cat "+ cat)
    # we are here because at least 2 items are present of this category in the wish list 
    # we need to find out the base price of these items
    # find how many pairs are there
    # sort these items by price
    # pick lower half and apply the discount
    
    items = []
    for i in range(0, len(cur_items)):
        it = cur_items[i]
        # need to check if this item is valid to be used in this
        # calculation
        isValid = is_not_on_discount(it) 
        if it["store"] == store and it["category"] == cat and isValid:
            items.append(it)
    logging.debug( items )        
    
    # how many pairs are useful?
    num_pairs = len(items)/2
    
    # sort based on price
    sorted_items = sorted(items, key=itemgetter('price'))
    logging.debug("Sorted items: " + str(sorted_items) )
    
    # calculate the discount
    discount = 0
    for i in range(0, num_pairs):
        price = sorted_items[i]["price"]
        info = "B1G1 discount calculation"
        sale_price = apply_discount(disc_rate, price, info)
        discount += (price - sale_price)
    return discount

def calculate_stw_step_discount(coup_discount, coup_threshold, cur_price):    
    coup_discount_perc = float(coup_discount/coup_threshold)
    savings = float (coup_discount_perc * cur_price)#apply_discount(coup_discount_perc, cur_price, "stw-step-disc")
    return savings

def aggregate_discount_check(coupon, total_price):
    
    # Algo:
    # 1. if (buy 1, get 1 discount exists)
    # 2.    count item stats for discount category
    # 3.    if (number of items in discount category > 1)
    # 4.        calculate, check for validity, and apply buy 1, get 1 discount
    # 5. if (store-wide dollar discount exists)
    # 6.    if (total_price > coupon_threshold)
    # 7.        calculate and apply discount
    
    logging.debug("aggr_disc: " + str(coupon["stw_discount_dollars"]) + " " + str(total_price))
    
    if ( coupon["item_spec_discount_type"] == "B1G1" and coupon["item_cat"] != "-"):
        # what category does this apply?
        cat = coupon["item_cat"]
        base_cat = find_base_category(cat)
        num_items_of_cat = item_stats[base_cat]
        logging.debug("aggr_disc: base_cat = " + str(base_cat) + 
                      " #of items of this cat: " + str(num_items_of_cat))
        if ( num_items_of_cat ) > 1:
            disc_rate = coupon["item_spec_discount_perc"]
            store = coupon["store"]
            discount_amount = calculate_b1g1_discount(store, cat, disc_rate)
            total_price -= discount_amount
    
    if coupon["stw_discount_dollars"] > 0:
        coup_thres = coupon["stw_discount_dollars_lower_bound"]  
        if total_price > coup_thres:
            coup_disc = coupon["stw_discount_dollars"]
            total_price -= calculate_stw_step_discount(coup_disc, coup_thres, total_price)
            
            logging.debug("aggr_disc: Total price reduced to " + str(total_price))            
        else:
            logging.debug("aggr_disc: Sorry. Buy for " + 
                          str(coupon["stw_discount_dollars_lower_bound"]-total_price) + 
                          "to get additional " + str(coupon["stw_discount_dollars"]) + " discount!") 
    else:
        logging.debug("aggr_disc: Sorry. No $X with $Y style discounts right now")

    return total_price
            

def check_shipping(coupon, total_price):
    if (total_price >= coupon["free_shipping_dollar_qualifier"]):
        logging.debug("ship_chk: Free shipping! Yay!")
        shipping_cost = 0
        return True
    else:
        logging.debug("ship_chk: Sorry, no Free Shipping")
        shipping_cost = DEFAULT_SHIPPING_COST         
        return False
    #return shipping_cost

def base_price(item1, item2):
    shipping_cost = DEFAULT_SHIPPING_COST
    base = float(item1["price"]) + float(item2["price"]) 
    logging.debug("base_price: " + str(base))
    return base

def current_sale_price(itemlist):
    sale = 0
    for i in range(0, len(itemlist)):
        sale += float(itemlist[i]["sale_price"])
    logging.debug("current_sale_price: " + str(sale))
    return sale

def category_match(cat1, cat2):
    if cat1 == cat2:
        return True

def apply_discount(disc, price, info):
    val = float(disc)
    p = float(price)
    res = p - p * val
    logging.debug("apply_disc: Discount: " + str(disc) + " Base price " + str(price) + " Sale price: " + str(res) + " " + info)
    return res

def match(coupon, item):
    # iterate over all items
    # same store
    if item["store"] == coupon["store"]:
        
        discount_applied = (item["sale_price"] < item["price"])
        
        logging.debug("stw-disc: " + str(coupon["stw_discount"]) + " disc-app: " + str(discount_applied))

        # First check store-wide discounts
        if coupon["stw_discount"] > 0 or (discount_applied == True): # and coupon["stw_discount_flag"] == 0:

            logging.debug("stw-disc: " + str(coupon["stw_discount"]) + " disc-app: " + str(discount_applied))
            discount_perc = float( (item["price"] - item["sale_price"]) / item["price"] )
            
            if (discount_perc == coupon["stw_discount"]):
                logging.debug("match: stw_discount already applied - " + str(discount_perc) + " " + str(coupon["stw_discount"]))
            else:
                logging.debug("match: stw_discount NOT applied - " + str(discount_perc) + " " + str(coupon["stw_discount"]))
                item["sale_price"] = apply_discount(coupon["stw_discount"], item["price"], "stw_disc")
            
            if coupon["add_stw_discount"] > 0:  # and coupon["add_stw_discount_flag"] == 0:
                item["sale_price"] = apply_discount(coupon["add_stw_discount"], item["sale_price"], "add_stw_disc")
          
        # same category
        if (category_match(coupon["item_cat"], item["category"])):
            item["sale_price"] = apply_discount(coupon["item_spec_discount_perc"], item["sale_price"], "item_disc")
                    
    return True

def match_express(coupon, item):

    # same store?
    if item["store"] == coupon["store"]:
        
        # For express, 
        #    stw_discount will be applied on applicable items already
        #       add_stw_discount should be applied to these items as shopstyle does not do this
        #    Per-item discounts typically of type: "buy 1, get 1" not reflected in item db.
        #       if coupon says "limited time" without expiry date, promotions could still be on.
        #       does not apply on stw_discounted items 

        discount_applied = (item["sale_price"] < item["price"]) # stw_discount applied alread
        logging.debug("stw-disc: " + str(coupon["stw_discount"]) + " disc-app: " + str(discount_applied))

        # Check coupon to see if discount applied should be store-wide or item-specific.
        # It cannot be both: needs to be verified
        # Algo:
        # 1. if there is stw_disc
        # 2.     if (stw_disc not applied)
        # 3.         apply_stw_disc
        # 5.     if (add_stw_disc)
        # 6.         apply_add_stw_disc
        # 7. else if there is item_specific disc
        # 8.     if (item in list matches that for which discount is available)
        # 9.         if (discount is of type: buy1, get1)
        # 10.            postpone for when discounts are checked across all items
        # 11.        else if (discount is of type: %-age off item)
        # 12.            if (discount_applied_already == false)
        # 13.                apply_item_spec_disc
        # 15.            if (add_stw_disc)
        # 16.                apply_add_stw_disc

        # Store-wide discounts
        if coupon["stw_discount"] > 0:

            if (discount_applied == True): # and coupon["stw_discount_flag"] == 0:

                discount_perc = float( (item["price"] - item["sale_price"]) / item["price"] )
            
                if (discount_perc == coupon["stw_discount"]):
                    logging.debug("match: stw_discount already applied - " + str(discount_perc) + " " + str(coupon["stw_discount"]))
                    if coupon["add_stw_discount"] > 0:  # and coupon["add_stw_discount_flag"] == 0:
                        item["sale_price"] = apply_discount(coupon["add_stw_discount"], item["sale_price"], "add_stw_disc")
                else:
                    logging.debug("match: Stated stw_discount NOT applied - " + str(discount_perc) + " " + str(coupon["stw_discount"]))

            else:
                item["sale_price"] = apply_discount(coupon["stw_discount"], item["price"], "stw_disc")

        elif coupon["item_spec_discount_perc"] > 0:

            # Category-specific discounts
            if (check_category_match(coupon["item_cat"], item["category"])):#category_match(coupon["item_cat"], item["category"])):

                # Check what kind of item-specific discount exists?
                if (coupon["item_spec_discount_type"] == "B1G1"):
                    # Apply in aggregage_discount_check
                    logging.debug("match: item-specific discount is buy1, get1. Postpone application to aggr_items round.")

                elif (coupon["item_spec_discount_type"] == "CSALE"):
                    logging.debug("match: item-specific discount is Sale. Apply discount")

                    if (discount_applied == True): # and coupon["stw_discount_flag"] == 0:
                        discount_perc = float( (item["price"] - item["sale_price"]) / item["price"] )            
                        if (discount_perc == coupon["item_spec_discount_perc"]):
                            logging.debug("match: item_specific_discount already applied - " + str(discount_perc) + " " + str(coupon["item_spec_discount_perc"]))
                            if coupon["add_stw_discount"] > 0:  # and coupon["add_stw_discount_flag"] == 0:
                                item["sale_price"] = apply_discount(coupon["add_stw_discount"], item["sale_price"], "add_stw_disc")
                        else:
                            logging.debug("match: Stated item_specific_discount NOT applied - " + str(discount_perc) + " " + str(coupon["item_spec_discount_perc"]))
                    else:
                        item["sale_price"] = apply_discount(coupon["item_spec_discount_perc"], item["sale_price"], "item_disc")
                    
    return True


def read_item_info(filename):
    #logging.debug("Processing " + filename
    f = open(filename, 'r')
    itemlist = []
    i = 0
    for line in f:
        itemdata_arr = line.split("|")
        price_arr = itemdata_arr[2].split(",")
        #if itemdata_arr[1].strip() == "mens-shirts":
            #logging.debug(itemdata_arr[0].strip(), itemdata_arr[1].strip(), price_arr[0].strip(), price_arr[1].strip()
        itemlist.append( {"store": itemdata_arr[0].strip(), 
                          "category": itemdata_arr[1].strip(), 
                          "price": float(price_arr[0].strip()),
                          "sale_price": float(price_arr[1].strip())} )
        i += 1

    #logging.debug(len(itemlist)        
    return itemlist

def calculate_item_stats(wish_list, item_stats):

    for i in range(0, len(wish_list)):
        it = wish_list[i]
        cat = it["category"]
        base_cat = find_base_category(cat)
        item_stats[base_cat] += 1

def check_category_match(cat1, cat2):
    base_cat1 = find_base_category(cat1)
    base_cat2 = find_base_category(cat2)
    result = (base_cat1 == base_cat2)
    return result

def find_base_category(category):
    jeans = category.lower().find("jeans".lower())
    sweater = category.lower().find("sweater".lower())
    pant = category.lower().find("pant".lower())
    shirt = category.lower().find("shirt".lower())
    
    if jeans > 0:
        return "jeans"
    if sweater > 0:
        return "sweater"
    if pant > 0:
        return "pant"
    if shirt > 0:
        return "shirt"

def init_item_stats(item_stats):
    item_stats["jeans"] = 0
    item_stats["sweater"] = 0
    item_stats["pant"] = 0
    item_stats["shirt"] = 0


def create_sample_wishlist(slist, user_config):
    
    #print len(store_itemlist)
    
    # 0: shirt, pant
    # 1: shirt, pant, jeans
    # 2: shirt, pant, jeans, jeans
    # 3: jeans, jeans, pant, sweater
    # 4: sweater, sweater, jeans, jeans
    # 5: sweater, shirt, pant, jeans, sweater
    
    items = []
    #wish_list = []
    
    if (user_config == 0):
        logging.info("Wishlist %d: 1 Men's Shirt, 1 Men's Pant", user_config)
        items.append(slist[MENS_SHIRTS][0]) 
        items.append(slist[MENS_PANTS][0])
    elif (user_config == 1):
        logging.info("Wishlist %d: 1 Men's Shirt, 2 Men's Pants", user_config)
        items.append(slist[MENS_SHIRTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
    elif (user_config == 2):
        logging.info("Wishlist %d: 1 Men's Shirt, 3 Men's Pants", user_config)
        items.append(slist[MENS_SHIRTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
    elif (user_config == 3):
        logging.info("Wishlist %d: 4 Men's Pants", user_config)
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
    elif (user_config == 4):
        logging.info("Wishlist %d: 2 Women's Sweaters, 1 Women's Jeans, 1 Men's Jeans", user_config)
        items.append(slist[WOMENS_SWEATERS][0])
        items.append(slist[WOMENS_SWEATERS][0])
        items.append(slist[MENS_JEANS][0])
        items.append(slist[WOMENS_JEANS][0])
    elif (user_config == 5):
        logging.info("Wishlist %d: 1 Men's Pants, 1 Men's Jean, 2 Women's Sweater, 1 Men's Shirt", user_config)
        items.append(slist[WOMENS_SWEATERS][0])
        items.append(slist[MENS_SHIRTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_JEANS][0])
        items.append(slist[WOMENS_SWEATERS][0])
    elif (user_config == 6):
        logging.info("Wishlist %d: 4 Men's Pants, 2 Men's Shirts, 1 Men's Jean, 1 Women's Sweater, 1 Women's Jean", user_config)
        items.append(slist[WOMENS_SWEATERS][0])
        items.append(slist[MENS_SHIRTS][0])
        items.append(slist[MENS_SHIRTS][0])
        items.append(slist[MENS_JEANS][0])
        items.append(slist[WOMENS_JEANS][0]) 
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
        items.append(slist[MENS_PANTS][0])
    

    #logging.debug(slist[0][0])
    #logging.debug(slist[1][0])
    
    #for i in range(0, len(slist)):
    #    wish_list.append(items[i])
    
    
    #print item_stats
    return items

if __name__ == "__main__":
    
    #log = logging.getLogger("MyApp")
    
    store_name = sys.argv[1] 
    sex_type = ["mens", "womens"]    
    category_arr = ["shirts", "pants", "jeans", "sweaters"]
    
    fname = []
    fcount = 0
    for i in range(0, len(sex_type)):
        for j in range(0, len(category_arr)):
            if ( ((i == 0) and (j < 3)) or ((i == 1) and (j > 1)) ):
                fstr = "../shopstyle-int/data/" + store_name + "-" + sex_type[i] + "-" + category_arr[j] + "-ss-" + "2011-12-24.data"
                fname.append(fstr)
                fcount += 1
    
    store_itemlist = []
    for i in range(0,fcount):
        store_itemlist.append(read_item_info(fname[i]))

    #logging.debug("Number of input arguments: " + str(len(sys.argv)-1)
    if ( store_name == "express" ):
        cur_coupon = coupon_express_dec_22
    elif ( store_name == "jcrew" ):
        cur_coupon = coupon_jcrew_dec_18
    
    item_stats = {}

    for j in range(0, 3):
        
        logging.debug("---- Iteration " + str(j) + " Start -----")
        
        dc_list = copy.deepcopy(store_itemlist)
        cur_items = create_sample_wishlist(dc_list, j)
        
        init_item_stats(item_stats)
        calculate_item_stats(cur_items, item_stats)
        
        #print cur_items
        
        cur_sale = current_sale_price(cur_items)

        #cur_coupon = coupon_jcrew_dec_18
        #cur_coupon = coupon_express_dec_22
        for i in range(0, len(cur_items)):
            match_express(cur_coupon, cur_items[i])
    
        #match_express(cur_coupon, item2)
        total_price = 0
        for i in range(0, len(cur_items)):
            total_price += float(cur_items[i]["sale_price"])
        #total_price = float(item1["sale_price"]) + float(item2["sale_price"])
        
        logging.debug("aggregate item price (after stw-disc and item-disc): " + str(total_price))
    
        total_price = aggregate_discount_check(cur_coupon, total_price)
        shipping_free = check_shipping(cur_coupon, total_price)
                
        logging.info("Original cost: " + str(cur_sale) + " Discounted cost: " + str(total_price) + " Savings: " + 
                 str(cur_sale-total_price) + " Free Shipping: " + str(shipping_free))
        
        logging.debug("---- Iteration " + str(j) + " Done -----")
        
