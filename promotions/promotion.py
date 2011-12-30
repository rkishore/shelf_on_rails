import sqlite3
import datetime

'''
    Representing a promo info item. This is a structured form of the coupons.
    - Store name
    - type [whole, whole-add, item-spec, aggregate]
    - validity till when?
    - code
    - where? store, online, both?

[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [TYPE:STORE-WIDE] [%] [DISC_AMOUNT] [DISC_LOWER_BOUND] [-] 
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [TYPE:ITEM-SPEC-B1-G1] [%] [AMOUNT] [CATEGORY_SEX] [CATEGORY_ITEM]
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE/STORE/BOTH] [TYPE:ITEM-SPEC-BUY-N-FOR-X] [N] [X] [CATEGORY_SEX] [CATEGORY_ITEM]
[STORE] [ISSUE] [VALIDITY] [CODE] [ONLINE] [TYPE:SHIPPING] [LOWER_BOUND] [0] [-] [-]

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
FREE_SHIPPING = 3

#ITEM_SPEC_CATEGORY
ITEM_SPEC_B1G1 = 4
ITEM_SPEC_BUY_N_FOR_X = 5

# Validity = number of days specified in the promo
TODAY_ONLY = 1
LIMITED_TIME = 30 # a month?

#ITEM CATEGORIES
SHIRTS = 1
PANTS = 2
JEANS = 3
SWEATERS = 4
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
class Promotion:
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
        
    def initialize_from_db_rows(self, rows):
        for row in rows:
            print row
            #print type(row)
            print row["store"]
            print row["d"]
            promo_type = row["promo_type"]
            print "Promo type: " + str(promo_type)
            self.promo_type = promo_type
            if promo_type == WHOLE_STORE_BASE_PERC:
                self._initialize_whole_store_base(row)
            elif promo_type == ITEM_SPEC_B1G1:
                self._intialize_item_spec_b1g1(row)
            elif promo_type == ITEM_SPEC_BUY_N_FOR_X:
                self._initialize_item_spec_buy_n_for_x(row)   
 
            
    def __str__(self):
        title = "STORE: ISSUE: VALID: CODE: AVAILAILITY: SHIPPING: "     
        val = self.store_name + " " + str(self.issue_date) + " " + str(self.validity) + " " + \
            self.code + " " + str(self.where) + " " + str(self.shipping) + " "
        
        if self.promo_type == WHOLE_STORE_BASE_PERC:
            title += "WHOLE_STORE_DISC WHOLE_STORE_AGGR WHOLE_STORE_AGGR_LOW_BOUND "
            val += str(self.whole_store_perc) + " " + str(self.whole_store_aggr_disc) + " " + \
                str(self.whole_store_aggr_low_bound) + " "
        if self.promo_type == ITEM_SPEC_B1G1:
            title += "ITEM_SPEC_B1G1_PERC ITEM_SPEC_B1G1_AMOUNT " 
            val += str(self.item_spec_b1g1_perc) + " " + str(self.item_spec_b1g1_amount) + " "
        if self.promo_type == ITEM_SPEC_BUY_N_FOR_X:
            title += "ITEM_SPEC_BUY_n_FOR_x_N ITEM_SPEC_BUY_n_FOR_x_X "
            val += str(self.item_spec_buy_n_for_x_X) + " " + str(self.item_spec_buy_n_for_x_N) + " "
            
        title += "SEX_CAT ITEM_CAT "
        val += str(self.sex_category) + " " + str(self.item_category) 
        return title + "\n" + val
        
#####################################################################
            
    
def put_promo_info_whole_store(store, date_issued, shipping, where, validity, code,
                               whole_store_perc, whole_store_aggr_disc, 
                               whole_store_aggr_low_bound, whole_store_add):
    
    promo = Promotion(store)
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
    
    promo = Promotion(store)
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

'''Returns a Promotion class instance for the given store & date '''
def get_promo_info(store, date_):    
    rows = _fetch_all_rows_date(store, date_)
    print type(rows)
    promo = Promotion(store)
    promo.initialize_from_db_rows(rows)
    #str(promo)
    print str(promo)
    return rows
    
    
    
#########################################################################    
''' Database specific functions '''

TABLE_NAME = "promoInfo"   
def _setup_db(location):
    # location will contain the data
    conn = sqlite3.connect(location, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()    
    _create_table(cursor)
    return (cursor, conn)

def _create_table(cursor):
    ''' set up promoInfo table if not already exists '''
    command = 'create table if not exists ' + TABLE_NAME + ' ( store text, d date, ' + \
            ' validity int, code text, where_avail int, free_shipping_lower_bound int,' + \
            ' promo_type int, promo_disc_perc int, promo_disc_amount int, promo_disc_lower_bound int, ' + \
            ' sex_category int, item_category int, ' + \
            ' PRIMARY KEY(store, d, promo_type, sex_category, item_category, promo_disc_perc, promo_disc_amount, promo_disc_lower_bound))'
            
    print command
    cursor.execute(command)

def _insert_row(store, date_, validity, code, where, free_shipping_lower_bound,   
                promo_type, disc_perc, disc_amount, disc_required_lower_bound, sex_category, item_category):
    
    
    
    '''values = "( \"" + store + "\", " + date_ + ", " + str(validity) + ", \"" + code + \
             "\", " + str(where) + ", " + str(free_shipping_lower_bound) + ", " + str(promo_type) + \
             ", " + str(disc_perc) + ", " + str(disc_amount) + ", " + str(disc_required_lower_bound) + \
             ", " + str(sex_category) + ", " + str(item_category) + " )"
   
    print values 
    command = 'insert into ' + TABLE_NAME + ' values ' + values 
    print command'''
    data = [store, date_, validity, code, where, free_shipping_lower_bound, promo_type,
            disc_perc, disc_amount, disc_required_lower_bound, sex_category, item_category]
    print "Inserting: " + str(data)
    #CURSOR.execute(command)
    CURSOR.execute('insert into promoInfo values(?,?,?,?,?,?,?,?,?,?,?,?)', data)
    
        
def _del_row(store, date_):
    CURSOR.execute('delete from promoInfo where store==? and d==?', (store, date_))
    

def _fetch_single_row_date(store, date_):
    CURSOR.execute('select * from promoInfo where store==? and d==?', (store, date_))
    return CURSOR.fetchone()

def _fetch_all_rows_date(store, date_):
    CURSOR.execute('select * from promoInfo where store==? and d==?', (store, date_))
    return CURSOR.fetchall()

def _fetch_all_rows(store):
    CURSOR.execute('select * from promoInfo where store==?', (store,))
    return CURSOR.fetchall()

'''
WHOLE_STORE_INFO ARGS: 1. store, 2. date_issued, 3. shipping, 4. where, 5. validity, 6. code,
                       6. whole_store_perc, 7. whole_store_aggr_disc, 7. whole_store_aggr_low_bound, 8. whole_store_add
                       
ITEM_SPEC_INFO ARGS: 1. store, 2. date_issued, 3. shipping, 4. where, 5. validity, 6. code,
                     6. sex_category, 7. item_category, 8. item_spec_b1g1_perc, 9. item_spec_b1g1_amount, 
                     9. item_spec_buy_n_for_x_N, 10. item_spec_buy_n_for_x_X
'''

def feed_jcrew_promos():
    store = "jcrew"
    date_issued = datetime.date(2011, 12, 6)
    
    sex_category = EVERYONE
    item_category = OUTERWEAR
    item_spec_b1g1_perc = 30
    item_spec_b1g1_amount = 0
    item_spec_buy_n_for_x_N = 0
    item_spec_buy_n_for_x_X = 0
    # what about shipping?
    validity = 2 # two days
    put_promo_info_item_spec(store, date_issued, 100, STORE_AND_ONLINE, validity, "CODE-2", sex_category, 
                             item_category, item_spec_b1g1_perc, item_spec_b1g1_amount, 
                             item_spec_buy_n_for_x_N, item_spec_buy_n_for_x_X)
    #return
    date_issued = datetime.date(2011, 12, 8)
    whole_perc_disc = 25 
    whole_aggr_disc = 0
    whole_aggr_disc_low_bound = 0
    whole_store_add = 0
    free_shipping_low_bound = 150
    validity = TODAY_ONLY
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
    #return
    date_issued = datetime.date(2011, 12, 12)
    whole_perc_disc = 25 
    whole_aggr_disc = 0
    whole_aggr_disc_low_bound = 0
    whole_store_add = 0
    free_shipping_low_bound = INFINITY
    validity = TODAY_ONLY
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
        
    date_issued = datetime.date(2011, 12, 13)
    whole_perc_disc = 0 
    whole_aggr_disc = 20
    whole_aggr_disc_low_bound = 100
    whole_store_add = 0
    free_shipping_low_bound = INFINITY
    validity = 7
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
    
    whole_aggr_disc = 25
    whole_aggr_disc_low_bound = 150
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
    
    whole_aggr_disc = 30
    whole_aggr_disc_low_bound = 250
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
 
    
    
    date_issued = datetime.date(2011, 12, 16)
    whole_perc_disc = 30 
    whole_aggr_disc = 0
    whole_aggr_disc_low_bound = 0
    whole_store_add = 0
    free_shipping_low_bound = 0
    validity = TODAY_ONLY
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
   
    date_issued = datetime.date(2011, 12, 17)
    whole_perc_disc = 30 
    whole_aggr_disc = 0
    whole_aggr_disc_low_bound = 0
    whole_store_add = 0
    free_shipping_low_bound = 100
    validity = TODAY_ONLY
    put_promo_info_whole_store(store, date_issued, free_shipping_low_bound, STORE_AND_ONLINE, validity, "CODE-1", 
                               whole_perc_disc, whole_aggr_disc, whole_aggr_disc_low_bound, whole_store_add)
 
    

if __name__ == "__main__":
    CURSOR, conn = _setup_db("./promoSenseDB")
    date_issued = datetime.date.today()
    
    '''
    feed_jcrew_promos()
    conn.commit()
    print "Read: " + str(_fetch_single_row_date("jcrew", date_issued))
    print "Read: " + str(_fetch_all_rows("jcrew"))
    
    print "Deleting.."
    _del_row("jcrew", date_issued)
    conn.commit()
    print "Read: " + str(_fetch_single_row_date("jcrew", date_issued))
    '''
    date_issued = datetime.date(2011, 12, 16)
    print get_promo_info("jcrew", date_issued)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    