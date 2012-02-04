from debra.models import Items, CategoryModel, ProductModel, ColorSizeModel

PROD_MODEL_BASED = 0
SHOPSTYLE_BASED = 1
NAME_BASED = 2

def find_wishlist_cat(wishlist, cat_scheme):
    
    print 'In find_wishlist_cat'
    wishlist_cat = []
    if (cat_scheme == PROD_MODEL_BASED):
        for i in wishlist:
            #print i['category']
            wishlist_cat.append(i['category'])
    return wishlist_cat

if __name__ == "__main__":
    
    print 'Testing'