
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

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
B1G1 = 1
CSALE = 2

coupon_jcrew = {"store": "J.Crew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "CODE1",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "CODE2",
                "item_cat": "mens-shirts", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 25, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 50, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": 100, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_jcrew_dec_22 = {"store": "J.Crew", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 175, "discount_shipping_rate": "None", "standard_shipping_rate": 8.95,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }
               
coupon_jcrew_dec_18 = {"store": "J.Crew", 
                "stw_discount": 0.3, "stw_discount_perc_code": "-",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "MUSTSHOP",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

coupon_express_dec_22 = {"store": "Express", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.2, "add_stw_discount_perc_code": "-",
                "item_cat": "mens-jeans", "item_spec_discount_type": B1G1, "item_spec_discount_perc": 0.5, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }


coupon_abercrombie_dec_22 = {"store": "ABERCROMBIE", 
                "stw_discount": 0.4, "stw_discount_perc_code": "15399",
                "add_stw_discount": 0, "add_stw_discount_perc_code": "-",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": INFINITY, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
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

coupon_aerie_dec_22 = {"store": "AERIE", 
                "stw_discount": 0, "stw_discount_perc_code": "-",
                "add_stw_discount": 0.4, "add_stw_discount_perc_code": "39427841",
                "item_cat": "-", "item_spec_discount_perc": 0.25, "item_spec_discount_perc_code": "CODE4",
                "stw_discount_dollars": 0, "stw_discount_dollars_lower_bound": 75, "stw_discount_dollars_code": "CODE3",
                "free_shipping_dollar_qualifier": 100, "discount_shipping_rate": "None", "standard_shipping_rate": 10,
                "free_returns_dollar_qualifier": INFINITY, "discount_return_rate": "None", "standard_return_rate": 10
                }

# Item = ["store name", "category", "price", "sale price"]

DEFAULT_SHIPPING_COST = 10 # Placeholder: Need to dynamically determine shipping cost    

def aggregate_discount_check(coupon, total_price):
    
    logging.debug("aggr_disc: " + str(coupon["stw_discount_dollars"]) + " " + str(total_price))
    if coupon["stw_discount_dollars"] > 0:
        if total_price > coupon["stw_discount_dollars_lower_bound"]:
            total_price -= coupon["stw_discount_dollars"]
            logging.debug("aggr_disc: Total price reduced to " + str(total_price))            
        else:
            logging.debug("aggr_disc: Sorry. Buy for " + str(coupon["stw_discount_dollars_lower_bound"]-total_price) + "to get additional " + str(coupon["stw_discount_dollars"]) + " discount!") 
    else:
        logging.debug("aggr_disc: Sorry. No $X with $Y style discounts right now")

    return total_price
            

def check_shipping(coupon, total_price):
    if (total_price >= coupon["free_shipping_dollar_qualifier"]):
        logging.debug("ship_chk: Free shipping! Yay!")
        shipping_cost = 0
    else:
        logging.debug("ship_chk: Sorry, no Free Shipping")
        shipping_cost = DEFAULT_SHIPPING_COST         
    return shipping_cost

def base_price(item1, item2):
    shipping_cost = DEFAULT_SHIPPING_COST
    base = float(item1["price"]) + float(item2["price"]) 
    logging.debug("base_price: " + str(base))
    return base

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
            if (category_match(coupon["item_cat"], item["category"])):

                # Check what kind of item-specific discount exists?
                if (coupon["item_spec_discount_type"] == str(B1G1)):
                    # Apply in aggregage_discount_check
                    logging.debug("match: item-specific discount is buy1, get1. Postpone application to aggr_items round.")

                elif (coupon["item_spec_discount_type"] == str(CSALE)):
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

        

if __name__ == "__main__":
    
    #logging.debug("Number of input item files: " + str(len(sys.argv)-1)

    store_itemlist = []
    for i in range(1,len(sys.argv)):
        store_itemlist.append(read_item_info(sys.argv[i]))

    logging.debug(store_itemlist[0][0])
    logging.debug(store_itemlist[1][0])
    
    for i in range(0, 1):
        
        item1 = store_itemlist[0][i]
        item2 = store_itemlist[1][i]
        base = base_price(item1, item2)

        cur_coupon = coupon_jcrew_dec_18
        match(cur_coupon, item1)
        match(cur_coupon, item2)

        total_price = float(item1["sale_price"]) + float(item2["sale_price"])
        logging.debug("aggregate item price (after stw-disc and item-disc): " + str(total_price))

        total_price = aggregate_discount_check(cur_coupon, total_price)
        shipping_cost = check_shipping(cur_coupon, total_price)
        total_price += shipping_cost

        logging.debug("Base cost: " + str(base) + " Discounted cost: " + str(total_price) + " Savings: " + str(base-total_price))
    
