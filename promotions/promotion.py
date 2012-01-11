import sqlite3
import datetime
import logging

#logging.basicConfig(format='%(message)s', level=logging.DEBUG)


'''
    A promo object. This is a structured form of the coupons.
    - Store name
    - type [whole, whole-add, item-spec, aggregate]
    - validity till when?
    - code
    - where? store, online, both?

We store each promo in a separate database row and a separate Promotion class variable in memory.

For discounts of type: "30% discount for every purchase"
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [FREE_SHIPPING_LOW_BOUND] [TYPE:STORE-WIDE] [%] [0] [0] [-] 

For discounts of type: "$15 off $50, $30 off $100, $60 off $200+"
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [FREE_SHIPPING_LOW_BOUND] [TYPE:STORE-WIDE] [0] [15] [50] [-]
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [FREE_SHIPPING_LOW_BOUND] [TYPE:STORE-WIDE] [0] [30] [100] [-]
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [FREE_SHIPPING_LOW_BOUND] [TYPE:STORE-WIDE] [0] [60] [200] [-]
 
For discounts of type: "Buy 1 and get 30% off of another for all jeans"
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [FREE_SHIPPING_LOW_BOUND] [TYPE:ITEM-SPEC-B1-G1] [%] [AMOUNT] [CATEGORY_SEX] [CATEGORY_ITEM]

For discounts of type: "Buy 4 socks for $25"
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [TYPE:ITEM-SPEC-BUY-N-FOR-X] [4] [25] [CATEGORY_SEX] [CATEGORY_ITEM]


TODO: (1) use sql's date syntax so that we can find appropriate entries using sql queries
NOTE: (1) For each store, we may have multiple entries per day. This is because we store each type of discount
          separately in different rows.
'''


#WHERE?
STORE_ONLY = 0
ONLINE_ONLY = 1
STORE_AND_ONLINE = 2

#WHOLE_STORE_CATEGORY
WHOLE_STORE_BASE_PERC = 0
WHOLE_STORE_AGGREGATE = 1
WHOLE_STORE_ADDITIONAL = 2

#ITEM_SPEC_CATEGORY
ITEM_SPEC_B1G1 = 3
ITEM_SPEC_BUY_N_FOR_X = 4

# Validity = number of days specified in the promo
TODAY_ONLY = 1
LIMITED_TIME = 30 # a month?

#ITEM CATEGORIES
SHIRTS = 1
PANTS = 2
SWEATERS = 3
JEANS = 4
OUTERWEAR = 5
UNDERWEAR = 6
EVERYTHING = 7

#SEX CATEGORIES
MALE = 0
FEMALE = 1
EVERYONE = 2

# used to make sure the lower bound is not met
INFINITY = 100000

#####################################################################

class Promotions:
    # list of PromotionUnit objects
    def __init__(self, store_name):
        self.store_name = store_name
        self.promoUnits = []

    def add_promo_obj(self, promo):
        self.promoUnits.append(promo)

    def how_many(self):
        return len(self.promoUnits)
        
    def __str__(self):
        result = ""
        for promo in self.promoUnits:
            #print promo
            result += str(promo) + "\n"
        return result

class PromotionObj:
    '''Base parent class'''
    def __init__(self, store_name):
        self.store_name = store_name
        

    def set_basic_info(self, issue_date, shipping, code, validity, where):
        self.issue_date = issue_date
        self.code = code
        self.validity = validity
        self.where = where
        self.shipping = shipping
        
    def set_store_wide(self, whole_store_perc, whole_store_aggr_disc,
                        whole_store_aggr_low_bound, whole_store_add):
        self.whole_store_perc = whole_store_perc
        self.whole_store_aggr_disc = whole_store_aggr_disc
        self.whole_store_aggr_low_bound = whole_store_aggr_low_bound
        self.whole_store_add = whole_store_add
        
    def set_item_specific(self, sex_category, item_category,
                          item_spec_b1g1_perc, item_spec_b1g1_amount,
                          item_spec_buy_n_for_x_N,
                          item_spec_buy_n_for_x_X):
        self.sex_category = sex_category
        self.item_category = item_category
        self.item_spec_b1g1_perc = item_spec_b1g1_perc
        self.item_spec_b1g1_amount = item_spec_b1g1_amount
        self.item_spec_buy_n_for_x_N = item_spec_buy_n_for_x_N
        self.item_spec_buy_n_for_x_X = item_spec_buy_n_for_x_X
        
    
   
    def _initialize_basic(self, row):
        self.store_name = row["store"]
        self.code = row["code"]
        self.issue_date = row["d"]
        self.validity = row["validity"]
        self.shipping = row["free_shipping_lower_bound"]
        self.where = row["where_avail"]
    
    def _initialize_whole_store_base(self, row):
        self._initialize_basic(row)
        self.whole_store_perc = row["promo_disc_perc"]
     
    def _initialize_whole_store_add(self, row):
        self._initialize_basic(row)
        self.whole_store_add = row["promo_disc_perc"]
           
    def _initialize_whole_store_aggr(self, row):
        self._initialize_basic(row)
        self.whole_store_aggr_disc = row["promo_disc_amount"]
        self.whole_store_aggr_low_bound = row["promo_disc_lower_bound"]
        self.sex_category = row["sex_category"]
        self.item_category = row["item_category"]
                        

    def _intialize_item_spec_b1g1(self, row):
        self._initialize_basic(row)
        self.item_spec_b1g1_perc = row["promo_disc_perc"]
        self.item_spec_b1g1_amount = row["promo_disc_amount"]
        self.item_category = row["item_category"]
        self.sex_category = row["sex_category"]
    
    def _initialize_item_spec_buy_n_for_x(self, row):
        self._initialize_basic(row)
        self.item_spec_buy_n_for_x_N = row["promo_disc_perc"]
        self.item_spec_buy_n_for_x_X = row["promo_disc_amount"]
        self.item_category = row["item_category"]
        self.sex_category = row["sex_category"]
        
    def initialize_from_db_row(self, row):
        print row
        promo_type = row["promo_type"]
        logging.debug("Promo type: " + str(promo_type))
        self.promo_type = promo_type
        if promo_type == WHOLE_STORE_BASE_PERC:
            self._initialize_whole_store_base(row)
        if promo_type == WHOLE_STORE_ADDITIONAL:
            self._initialize_whole_store_add(row)
        elif promo_type == WHOLE_STORE_AGGREGATE:
            self._initialize_whole_store_aggr(row)
        elif promo_type == ITEM_SPEC_B1G1:
            self._intialize_item_spec_b1g1(row)
        elif promo_type == ITEM_SPEC_BUY_N_FOR_X:
            self._initialize_item_spec_buy_n_for_x(row)   
 
    '''
    This method initializes from django's object manager object
    '''
    def initialize(self, db_obj):
        self.store_name = db_obj.store
        self.issue_date = db_obj.d
        self.validity = db_obj.validity
        self.where = db_obj.where_avail
        self.promo_type = db_obj.promo_type
        
        self.code = db_obj.code
        self.sex_category = db_obj.sex_category
        self.item_category = db_obj.item_category
        self.shipping = db_obj.free_shipping_lower_bound
        self.item_spec_discount_type = db_obj.promo_type

        if db_obj.promo_type == WHOLE_STORE_BASE_PERC:
            self.whole_store_perc = float(db_obj.promo_disc_perc/100.0)
            
        if db_obj.promo_type == WHOLE_STORE_AGGREGATE:
            self.whole_store_aggr_disc = db_obj.promo_disc_amount
            self.whole_store_aggr_low_bound = db_obj.promo_disc_lower_bound
            
        if db_obj.promo_type == WHOLE_STORE_ADDITIONAL:
            self.whole_store_add = float(db_obj.promo_disc_perc/100.0)
            
        if db_obj.promo_type == ITEM_SPEC_B1G1:
            self.item_spec_b1g1_perc = float(db_obj.promo_disc_perc/100.0)
            self.item_spec_b1g1_amount = db_obj.promo_disc_amount            
            
            
        if db_obj.promo_type == ITEM_SPEC_BUY_N_FOR_X:
            self.item_spec_buy_n_for_x_N = float(db_obj.promo_disc_perc)
            self.item_spec_buy_n_for_x_X = db_obj.promo_disc_amount
                
            
    def __str__(self):
        title = "STORE: ISSUE: VALID: CODE: AVAILAILITY: SHIPPING: "     
        val = str(self.store_name) + " " + str(self.issue_date) + " " + str(self.validity) + " " + \
            self.code + " " + str(self.where) + " " + str(self.shipping) + " "
        
        if self.promo_type == WHOLE_STORE_BASE_PERC:
            title += "WHOLE_STORE_DISC "
            val += str(self.whole_store_perc) + " " 
        if self.promo_type == WHOLE_STORE_AGGREGATE:
            title += "WHOLE_STORE_AGGR WHOLE_STORE_AGGR_LOW_BOUND "
            val += str(self.whole_store_aggr_disc) + " " + \
                str(self.whole_store_aggr_low_bound) + " "
        if self.promo_type == WHOLE_STORE_ADDITIONAL:
            title += "WHOLE_STORE_ADDITIONAL "
            val += str(self.whole_store_add) + " "
        if self.promo_type == ITEM_SPEC_B1G1:
            title += "ITEM_SPEC_B1G1_PERC ITEM_SPEC_B1G1_AMOUNT " 
            val += str(self.item_spec_b1g1_perc) + " " + str(self.item_spec_b1g1_amount) + " "
        if self.promo_type == ITEM_SPEC_BUY_N_FOR_X:
            title += "ITEM_SPEC_BUY_n_FOR_x_N ITEM_SPEC_BUY_n_FOR_x_X "
            val += str(self.item_spec_buy_n_for_x_X) + " " + str(self.item_spec_buy_n_for_x_N) + " "
        
        if (self.promo_type == ITEM_SPEC_B1G1 or self.promo_type == ITEM_SPEC_BUY_N_FOR_X): 
            title += "SEX_CAT ITEM_CAT "
            val += str(self.sex_category) + " " + str(self.item_category) 
        return title + "\n" + val
        
#####################################################################
            
    
def put_promo_info_whole_store(store, date_issued, shipping, where, validity, code,
                               whole_store_perc, whole_store_aggr_disc, 
                               whole_store_aggr_low_bound, whole_store_add):
    
    promo = PromotionObj(store)
    promo.set_basic_info(date_issued, shipping, code, validity, where)
    promo.set_store_wide(whole_store_perc, whole_store_aggr_disc, 
                          whole_store_aggr_low_bound, whole_store_add)
    
    ''' store this in a DB'''
    _insert_row(store, date_issued, validity, code, where, shipping, 
                WHOLE_STORE_BASE_PERC,
                whole_store_perc, 
                whole_store_aggr_disc, whole_store_aggr_low_bound, 
                EVERYONE, EVERYTHING)

def put_promo_info_item_spec(store, date_issued, shipping, where, validity, code,
                             sex_category, item_category, 
                             item_spec_b1g1_perc, item_spec_b1g1_amount, 
                             item_spec_buy_n_for_x_N, item_spec_buy_n_for_x_X):
    
    promo = PromotionObj(store)
    promo.set_basic_info(date_issued, shipping, code, validity, where)
    promo.set_item_specific(sex_category, item_category, 
                            item_spec_b1g1_perc, item_spec_b1g1_amount, 
                            item_spec_buy_n_for_x_N, item_spec_buy_n_for_x_X)

    _insert_row(store, date_issued, validity, code, where, shipping,
                ITEM_SPEC_B1G1, 
                item_spec_b1g1_perc,
                item_spec_b1g1_amount,
                0,
                sex_category, item_category)
    
    _insert_row(store, date_issued, validity, code, where, shipping, 
                ITEM_SPEC_BUY_N_FOR_X,
                item_spec_buy_n_for_x_N, item_spec_buy_n_for_x_X,
                0,
                sex_category, item_category)


def create_new_promo(promos, store):
    #print promos
    promotions = Promotions(store)
    
    for promo in promos:
        p = PromotionObj(store)
        p.initialize(promo)
        promotions.add_promo_obj(p)

    return promotions

'''Returns a list of Promotion class instances for the given store & date '''
def get_promo_info_date(store, date_):    
    rows = _fetch_all_rows_date(store, date_)
    logging.debug("GET_PROMO_INFO: " + str(type(rows)))
    promotions = Promotions(store)
    for row in rows:
        promo = PromotionObj(store)
        promo.initialize_from_db_row(row)
        print str(promo)
        promotions.add_promo_obj(promo)
        
    logging.debug("GET_PROMO_INFO: promotions " + str(promotions))
    return promotions
    

def get_promo_info(store):    
    rows = _fetch_all_rows(store)
    logging.debug("GET_PROMO_INFO: " + str(type(rows)))
    promotions = Promotions(store)
    
    for row in rows:
        promo = PromotionObj(store)
        promo.initialize_from_db_row(row)
        print str(promo)
        promotions.add_promo_obj(promo)
        
    logging.debug("GET_PROMO_INFO: promotions " + str(promotions))
    print "How many? " + str(promotions.how_many())
    return promotions
    
    
    
#########################################################################    
''' Database specific functions '''

TABLE_NAME = "promoInfo"   
def _setup_db(location):
    # location will contain the data
    conn = sqlite3.connect(location, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()    
    #_create_table(cursor)
    return (cursor, conn)

# Not needed
def _create_table(cursor):
    ''' set up promoInfo table if not already exists '''
    command = 'create table if not exists ' + TABLE_NAME + ' ( store text, d date, ' + \
            ' validity int, code text, where_avail int, free_shipping_lower_bound int,' + \
            ' promo_type int, promo_disc_perc int, promo_disc_amount int, promo_disc_lower_bound int, ' + \
            ' sex_category int, item_category int, ' + \
            ' PRIMARY KEY(store, d, promo_type, sex_category, item_category, promo_disc_perc, promo_disc_amount, promo_disc_lower_bound))'
            
    logging.debug(command)
    cursor.execute(command)

def _insert_row(store, date_, validity, code, where, free_shipping_lower_bound,   
                promo_type, disc_perc, disc_amount, 
                disc_required_lower_bound, sex_category, item_category):

    data = [store, date_, validity, code, where, free_shipping_lower_bound, promo_type,
            disc_perc, disc_amount, disc_required_lower_bound, sex_category, item_category]
    logging.DEBUG("Inserting: " + str(data))
    #CURSOR.execute(command)
    CURSOR.execute('insert into promoInfo values(?,?,?,?,?,?,?,?,?,?,?,?)', data)
    
        
def _del_row(store, date_):
    CURSOR.execute('delete from promoInfo where store==? and d==?', (store, date_))
    


def _fetch_all_rows_date(store, date_):
    initialize()
    CURSOR.execute('select * from polls_promoinfo where store==? and d==?', (store, date_))
    return CURSOR.fetchall()

def _fetch_all_rows(store):
    initialize()
    CURSOR.execute('select * from polls_promoinfo where store==?', (store,))
    return CURSOR.fetchall()

def initialize():
    global CURSOR
    CURSOR, conn = _setup_db("../tutorial/testDB")
    return CURSOR

if __name__ == "__main__":
    #CURSOR, conn = _setup_db("./promoSenseDB")
    CURSOR, conn = _setup_db("../tutorial/testDB")
    
    date_issued = datetime.date.today()
    
    date_issued = datetime.date(2012, 1, 1)
    print date_issued
    logging.debug(get_promo_info("JCREW"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    