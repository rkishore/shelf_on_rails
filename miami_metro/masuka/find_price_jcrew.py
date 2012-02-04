from debra.models import StoreItemCombinationResults
from debra.models import Promoinfo, Items, Brands, Categories, ProductModel
from debra.models import CategoryModel, ColorSizeModel, WishlistI, UserIdMap
from debra.models import Promoinfo
from selenium import webdriver
from time import sleep
import datetime

ZIP_CODE = "08902"
PROMO_CODE = "RAJA"
STORE_ID_EXPRESS = 1
STORE_ID_JCREW = 2

def get_promo_codes(store_id):
    date_ = datetime.date.today()
    promo_date = Promoinfo.objects.filter(d = date_)
    promo = promo_date.filter(store__id = store_id).order_by('code').distinct('code')
    print promo
    print date_
    codes = set()
    for p in promo:
        codes.add(str(p.code))
    return codes


def calculate_price_for_express(wishlist_express):
    driver = webdriver.Firefox()

    codes = get_promo_codes(STORE_ID_EXPRESS)
    print "CODES: " + str(codes)
    print "Calculate_price for Express: " + str(wishlist_express)
    orig_cost_without_promo = 0
    for wi in wishlist_express:
        print "URL " + str(wi.item.prod_url)
        #add_url_to_cart(wi.item.prod_url)
        driver.get(wi.item.prod_url)
        
        prodid = wi.item.idx
        prodsize = wi.size
        print str(prodid)
        print str(prodsize)
        alloptions = driver.find_element_by_xpath('//select[@id="Size' + str(prodid) + 'Variants"]//option[@value="' + prodsize + '"]')
        alloptions.click()
        sleep(2)
        
        prodcolor = wi.color
        print str(prodcolor)
        colors = driver.find_elements_by_xpath('//img[@alt="' + prodcolor + '"]')
        if len(colors) > 0:
            colors[0].click()
            print "Sleeping for 2 sec"
            print colors
            sleep(2)

        addtobag = driver.find_element_by_xpath('//img[@alt="Add To Bag"]')        
        addtobag.click()
        print addtobag
        print "Sleeping for 2 sec"
        sleep(2)
        
        orig_cost_without_promo += wi.item.price
    
    cart = driver.find_element_by_xpath('//a[@id="widget-ucart-but"]')
    cart.click()
    sleep(2)
    
    for code in codes:
        promo_code = driver.find_element_by_xpath('//input[@id="che-bas-promoCode"]')
        promo_code.send_keys(code)
        sleep(2)
    
        promo_apply = driver.find_element_by_xpath('//img[@alt="Apply"]')
        promo_apply.click()
        sleep(2)
    
    summary_text = driver.find_elements_by_xpath('//dd')
    total_entries = len(summary_text)
    
    estimated_total = float(str(summary_text[total_entries - 1].text).replace('$', ''))
    estimated_shipping = 0
    
    if total_entries > 2:
        val = float(str(summary_text[total_entries - 2].text).replace('$', ''))
        total_without_shipping = 0
        if val < 0:
            promo_code_savings = 0 - val
            total_without_shipping = float(str(summary_text[total_entries-3].text).replace('$', ''))
        else:
            total_without_shipping = float(str(summary_text[total_entries - 2].text).replace('$', ''))

        print "Promo_code savings:" + str(promo_code_savings)
        print "TOtal without shippping: " + str(total_without_shipping)
        estimated_shipping = estimated_total + promo_code_savings - total_without_shipping
            
            
    promotion_val = orig_cost_without_promo - estimated_total
    estimated_tax = 0
    
    print "Estimated Total: " + str(estimated_total)
    print "Promotion Savings: " + str(promotion_val)
    print "Estimated Tax: " + str(estimated_tax)
    print "Estimated Shipping: " + str(estimated_shipping) 
    
    free_shipping = True
    if estimated_shipping > 0:
        free_shipping = False
        
    itemlist = []
    itemlist.append( {"orig_cost": orig_cost_without_promo, 
                      "total_cost": estimated_total, 
                      "savings": promotion_val,
                      "shipping": free_shipping,})
    driver.quit()
    return itemlist


def calculate_price_for_jcrew(wishlist_jcrew):
    driver = webdriver.Firefox()

    codes = get_promo_codes(STORE_ID_JCREW)
    print "CODES: " + str(codes)
    print "Calculate_price for J.Crew: " + str(wishlist_jcrew)
    orig_cost_without_promo = 0
    for wi in wishlist_jcrew:
        print "URL " + str(wi.item.prod_url)
        #add_url_to_cart(wi.item.prod_url)
        driver.get(wi.item.prod_url)
        
        prodsize = wi.size
        size = driver.find_element_by_xpath('//option[@value="' + prodsize + '"]')
        size.click()
        sleep(2)
        
        prodcolor = wi.color
        color = driver.find_element_by_xpath('//option[@value="' + prodcolor + '"]')
        color.click()
        print "Sleeping for 2 sec"
        print color
        sleep(2)

        cart = driver.find_element_by_xpath('//a[contains (@onclick, "AddToCart")]')
        cart.click()
        print cart
        print "Sleeping for 2 sec"
        sleep(2)
        orig_cost_without_promo += wi.item.price
            
    checkout = driver.find_element_by_xpath('//img[@alt="Checkout"]')
    checkout.click()
    sleep(2)
    
    
    
    # TAX
    #tax_zip = driver.find_element_by_xpath('//input[@id="tax_postal"]')
    #tax_zip.send_keys(ZIP_CODE)
    #sleep(2)
    
    #calc_tax = driver.find_element_by_xpath('//input[@alt="calculate tax"]')
    #calc_tax.click()
    #sleep(2)
    
    # PROMOTION
    for code in codes:
        promo_code = driver.find_element_by_xpath('//input[@id="promotionCode"]')
        promo_code.send_keys(code)
        sleep(2)
        
        promo_code_button = driver.find_element_by_xpath('//input[@alt="add promo"]')        
        promo_code_button.click()
        sleep(2)
    
    
    # SUMMARY
    '''NOTE that we are using "_elementS_" '''
    summary_text = driver.find_elements_by_xpath('//td[contains (@class, "total")]')
    total_entries = len(summary_text)
    
    estimated_total = float(str(summary_text[total_entries-1].text).replace('$', ''))
    
    promotion_val = float(str(summary_text[total_entries - 3].text).replace('$', '').replace('(', '').replace(')', ''))
    
    #estimated_tax = float(str(summary_text[total_entries -5].text).replace('$', ''))
    
    estimated_shipping = float(str(summary_text[total_entries - 7].text).replace('$', ''))
    
    print "Estimated Total: " + str(estimated_total - estimated_shipping)
    print "Original Cost: " + str(orig_cost_without_promo)
    print "Savings without promo: " + str(orig_cost_without_promo - (estimated_total - estimated_shipping))
    print "Promotion Savings: " + str(promotion_val)
    total_savings = promotion_val + (orig_cost_without_promo - (estimated_total - estimated_shipping))
    print "Total savings: " + str(total_savings)
    #print "Estimated Tax: " + str(estimated_tax)
    print "Estimated Shipping: " + str(estimated_shipping)
    free_shipping = True
    if estimated_shipping > 0:
        free_shipping = False
    itemlist = []
    itemlist.append( {"orig_cost": orig_cost_without_promo, 
                      "total_cost": estimated_total - estimated_shipping, 
                      "savings": total_savings,
                      "shipping": free_shipping,})
    driver.quit()
    return itemlist



def calculate_price_for_wishlist(userid):
    
    u = UserIdMap.objects.filter(user_id=userid)
    result = {} 
    print u
    print userid
    driver = webdriver.Firefox()
    if u:
        print 'User ID: ', u[0].user_id, 'IP: ', u[0].ip_addr 
        final_list = WishlistI.objects.filter(user_id=u[0])
        store_list_express = []
        store_list_jcrew = []
        for wi in final_list:
            print "WI.ITEM: " + str(wi.item)
            if wi.item.brand.name == "Express":
                store_list_express.append(wi)
            if wi.item.brand.name == "J.Crew":
                store_list_jcrew.append(wi)
        if len(store_list_express) > 0:
            result["Express"] = calculate_price_for_express(driver, store_list_express)
        if len(store_list_jcrew) > 0:
            result["J.Crew"] = calculate_price_for_jcrew(driver, store_list_jcrew)
    driver.quit()
    return result
    
if __name__ == "__main__":
    calculate_price_for_wishlist(6)