import re

# A coupon class contains following
# - store name
# - date issued
# - valid for X days
# - availability
# - applicability
# - type
class Coupon:
    
    def __init__(self, store_name, date_issued):
        self.store_name = store_name
        self.date_issued = date_issued
        self.code = ""
        self.validity = ""
        self.availability = ""
        self.applicability = ""
        self.type = ""
        self.shipping = ""
        
    def availability_info(self, new_info):
        self.availability += new_info
        
    def applicability_info(self, new_info):
        self.applicability += new_info
        
    def validity_info(self, new_info):
        self.validity += new_info
        
    def shipping_info(self, new_info):
        self.shipping += new_info
        
    def type_info(self, new_info):
        self.type += new_info
        
    def __str__(self):
        msg = self.store_name + " " + self.date_issued + " "  + self.code + " " + self.type + " " + self.validity + " " + self.availability+ " " + self.applicability + " " + self.shipping
        return msg
    
USERNAME = "rootofsavvypurse"
DST_LOCATION = "../../COUPON_EMAIL_DATA_TEXT_PART/" + USERNAME
DATE = "17Dec2011"
FILENAME = DST_LOCATION + "/" + DATE  + "/18_37_14_J.Crew"        

months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
availability_keywords = ["IN STORES & ONLINE", "IN STORES ONLY", "ONLINE ONLY", 
                         "IN-STORE", "IN STORES AND ONLINE"]
shipping_keywords = ["DAYS LEFT", "SHIP", "ORDER BY"]
applicability_keywords = ["EVERY PURCHASE", "ANY ORDER", "EVERY ORDER"]

# regular expression for dealing with subject
# example 1: CROSS IT ALL OFF: 30% OFF EVERY PURCHASE, IN STORES & ONLINE (PLUS, FREE SHIPPING)
# example 2: Happy holidays: 30% OFF every purchase, in stores & online (PLUS, FREE SHIPPING on every order)
# example 3: Unwrap more: UP TO 30% OFF, plus FREE SHIPPING on any order! Online only.
# example 4: Stuff those stockings: UP TO 30% OFF your order, ONLINE ONLY
# example 5: Give great gifts: UP TO 30% OFF your order, ONLINE ONLY
# example 6: Special delivery: 25% OFF EVERY ONLINE ORDER, TODAY ONLY
# example 7: Ends tomorrow: 25% OFF & FREE SHIPPING on orders of $150+
# example 8: Gifts galore: 25% OFF & FREE SHIPPING (plus, even more savings)
# example 9: Get gifting: 25% OFF & FREE SHIPPING on orders of $150+
# example 10: Chill factor: 30% OFF & FREE SHIPPING on all women's, men's and kids' outerwear
def process_subject(sub):
    #print sub
    s1 = sub.split(':')
    #print s1
    #s1[1] has all the interesting data
    # split at the first ","
    loc = s1[2].find(",")
    
    discount_info = s1[2][0: loc]
    #print "Discount: " + discount_info
    
    other_info = s1[2][loc+1: len(s1[2])]
    return (discount_info, other_info)
        
def process_body(body):
    return True

def process_sender(sender):
    #print "Sender: " + sender
    return "J.CREW"

def month_in_int(month_in_str):        
    MONTH_IN_STR = month_in_str.upper()
    loc = months.index(MONTH_IN_STR)
    return loc+1

    
def process_date(date):
    date = str(month_in_int(date[3])) + "." + date[2] + "." + date[4]
    #print "Date: " + date 
    return date        

def process_shipping(shipping):
    return True

def process_discount(discount):
    # regular expression for discount
    # words X% OFF words
    #DISCOUNT_REG_EX = "\A[\d]+%"
    d = discount.lstrip(' ')
    #print d

    words = d.split(' ')
    if words[0] == "UP TO":
        result = words[0] + " " + words[1]
    elif words[1] == "OFF":
        result = words[0]    
    else:
        result = "ERROR"    
    #print result
    return result

def process_availability(info):
    for i in range(0, len(availability_keywords)):
        keyword = availability_keywords[i]
        count = info.find(keyword)
        #print "Searching " + keyword + " in " + info + " res " + str(count)
        if count > 0:
            #print keyword
            return keyword
    result = "ERROR"    
    return result

def process_applicability(info):
    
    for i in range(0, len(applicability_keywords)):
        keyword = applicability_keywords[i]
        count = info.find(keyword)
        #print "Searching " + keyword + " in " + info + " res " + str(count)
        if count > 0:
            #print keyword
            return keyword
    result = "ERROR"    
    return result
        

def analyze_coupon(FILENAME):    
    fp = open(FILENAME)
    BODY = "" 
    
    # Analyze header info in the first pass
    for l0 in fp.readlines():
        LINE = l0.upper()    
        words = LINE.split(' ')
        if words[0] == "FROM:":
            sender = process_sender(words[1])
        elif words[0] == "SUBJECT:":
            discount_info, other_info = process_subject(LINE)
        elif words[0] == "DATE:":
            date = process_date(words)
        else:
            BODY += LINE
        
    fp.close()    
    print BODY
    
    coupon = Coupon(sender, date)    
    
    coupon.type_info(process_discount(discount_info))
    coupon.applicability_info(process_applicability(discount_info))
    coupon.availability_info(process_availability(other_info))
    process_shipping(other_info)
                
    print coupon
    
 
def replace_shipping(body):
    regex1 = "FREE SHIPPING"    
    exists = re.search(regex1, body)
    if exists != None:
        val = regex1
        res1 = re.sub(regex1, "<SHIPPING>", body)
        #print res1
        return (val, res1)
    return ("None", body)

#\bon\b[\w ]+\border[s]*\b[ \w\$+]*
    
def replace_applicability(body):
    regex1 = "ON ALL [ \w]*"
    exists = re.search(regex1, body)
    app = ""
    res1 = body
    if exists != None:
        val = exists.group(0)
        res1 = re.sub(regex1, "<ITEM>", body)
        app += val
    
    regex2 = "[\w ]+PURCHASE"
    exists = re.search(regex2, res1)    
    res2 = res1
    if exists != None:
        val = exists.group(0)
        res2 = re.sub(regex2, "<ITEM>", res1)
        app += ", " + val
        
    regex3 = "ORDERS OF [\w\$\d]+"
    exists = re.search(regex3, res2)
    res3 = res2
    if exists != None:
        val = exists.group(0)
        res3 = re.sub(regex3, "<BUDGET-QUALIFIER>", res2)
        app += ", " + val
    #print res3 
    #print app
    return (app, res3)   
    
def replace_discount(body):
    regex1 = "[\d]+% OFF"
    regex2 = "[\d]+% DISCOUNT"
    #disc = re.compile(regex)
    exists = re.search(regex1, body)
    if exists != None:
        val = exists.group(0).split(' ')
        disc = val[0]#.strip('%')
        #print disc 
        res1 = re.sub(regex1, "<DISCOUNT>", body)
        return (disc, res1)
    else:
        exists = re.search(regex2, body)
        val = exists.group(0).split(' ')
        disc = val[0]#.strip('%')
        #print disc
        res2 = re.sub(regex2, "<DISCOUNT>", res1)
        return (disc, res2)
    #print res2
    return ("0", res2)

def replace_availability(body):
    regex1 = "IN STORES & ONLINE"
    exists = re.search(regex1, body)
    if exists != None:
        val = regex1
        res1 = re.sub(regex1, "<AVAILABILITY>", body)
        #print res1
        return (val, res1)
    return ("none", body)
    
def replace_validity(body):
    # Assuming these keywords are used exclusively
    regex1 = "TODAY ONLY"
    exists = re.search(regex1, body)
    res1 = body
    if exists != None:
        val = regex1
        res1 = re.sub(regex1, "<VALIDITY>", body)
        return (val, res1)
    
    regex2 = "ENDS TOMORROW"
    res2 = res1
    exists = re.search(regex2, res1)
    if exists != None:
        val = regex2
        res2 = re.sub(regex2, "<VALIDITY>", res1)
        return (val, res2)
    
    # regular expression to catch Dec 18 2011
    regex3 = "[\w,]+\s\d[\d]?[,]*\s[\d]+"
    res3 = res2
    exists = re.search(regex3, res2)
    if exists != None:
        val = exists.group(0)
        res3 = re.sub(regex3, "<VALIDITY>", res2)
        return (val, res3)
    
    
    # regular expression to catch: 12/21 or 12.21
    regex4 = "[\d]+[\/.][\d]+"
    exists = re.search(regex4, res3)
    if exists != None:
        val = exists.group(0)
        res4 = re.sub(regex4, "<DATE>", res3)
        return (val, res4)
    #print res4
    return ("None", body)

def replace_code(body):    
    regex1 = "USE CODE [\w]+[.]*"
    
    exists = re.search(regex1, body)
    if exists != None:
        val = exists.group(0).split(' ')
        code = val[len(val)-1].strip('.')
        #print code
        res1 = re.sub(regex1, "<CODE>", body)
        #print res1
        return (code, res1)
    return ("none", body)
            
def replace_shipping_fineprint(body):
    regex = "\*SHIPPING[\S\s]*?\)\."
    res1 = re.sub(regex, "<SHIPPING_HANDLING_FINEPRINT>", body)
    #print res1
    return res1       

def replace_remaining_fineprint(body):
    regex = "\*\*OFFER[\S\s]*CHANGE\."
    res1 = re.sub(regex, "<DISCOUNT_FINEPRINT>", body)
    #print res1
    return res1 

def replace_mailing_list_info(body):
    regex = "PLEASE[\S\s]*"
    res1 = re.sub(regex, "<MAILING_LIST_INFO>", body)
    #print res1
    return res1 
 
if __name__ == "__main__":
    fp = open(FILENAME)
    BODY = ""
    
    for l0 in fp.readlines():
        LINE = l0.upper()    
        BODY += LINE
        
    fp.close()
    #print BODY 
    
    disc, B1 = replace_discount(BODY)
    ship, B2 = replace_shipping(B1)
    app, B3 = replace_applicability(B2)
    avail, B4 = replace_availability(B3)
    val, B5 = replace_validity(B4)
    CODE, B6 = replace_code(B5)
    B7 = replace_shipping_fineprint(B6)
    B8 = replace_remaining_fineprint(B7)
    B9 = replace_mailing_list_info(B8)
    print B9
    print "Jcrew " + " [" + disc + "] [" + app + "] [" + avail + "] [" + val + "] [" + ship + "] [" + CODE + "]"
    
    