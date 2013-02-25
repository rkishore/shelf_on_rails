# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SSItemStats'
        db.create_table('polls_ssitemstats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tdate', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 1, 22, 7, 54, 32, 96999))),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', to=orm['polls.Brands'])),
            ('category', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=20)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('price_selection_metric', self.gf('django.db.models.fields.IntegerField')(default='0')),
            ('price', self.gf('django.db.models.fields.FloatField')(default='-111.00', max_length=10)),
            ('saleprice', self.gf('django.db.models.fields.FloatField')(default='-111.00', max_length=10)),
            ('total_cnt', self.gf('django.db.models.fields.IntegerField')(default='-11', max_length=10)),
            ('sale_cnt', self.gf('django.db.models.fields.IntegerField')(default='-11', max_length=10)),
        ))
        db.send_create_signal('polls', ['SSItemStats'])


    def backwards(self, orm):
        
        # Deleting model 'SSItemStats'
        db.delete_table('polls_ssitemstats')


    models = {
        'polls.brands': {
            'Meta': {'object_name': 'Brands'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'})
        },
        'polls.categories': {
            'Meta': {'object_name': 'Categories'},
            'brand': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['polls.Brands']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'})
        },
        'polls.categorymodel': {
            'Meta': {'object_name': 'CategoryModel'},
            'categoryId': ('django.db.models.fields.IntegerField', [], {'default': "'Nil'", 'max_length': '50'}),
            'categoryName': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.ProductModel']"})
        },
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.colorsizemodel': {
            'Meta': {'object_name': 'ColorSizeModel'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.ProductModel']"}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'})
        },
        'polls.demand': {
            'Meta': {'object_name': 'Demand'},
            'gender': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_jeans': ('django.db.models.fields.IntegerField', [], {}),
            'num_shirts': ('django.db.models.fields.IntegerField', [], {}),
            'num_skirts': ('django.db.models.fields.IntegerField', [], {}),
            'num_sweaters': ('django.db.models.fields.IntegerField', [], {}),
            'total_items': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.itemlist': {
            'Meta': {'object_name': 'ItemList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item1': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist1'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item10': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist10'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item11': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist11'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item12': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist12'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item13': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist13'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item14': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist14'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item15': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist15'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item16': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist16'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item2': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist2'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item3': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist3'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item4': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist4'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item5': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist5'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item6': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist6'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item7': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist7'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item8': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist8'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'item9': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist9'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.Items']"}),
            'total_items': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        'polls.items': {
            'Meta': {'object_name': 'Items'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'cat1': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'cat2': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'cat3': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'cat4': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'cat5': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url_lg': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'img_url_md': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'img_url_sm': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_colors': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_currency': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_instock': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '10'}),
            'pr_retailer': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_sizes': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_url': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'20.00'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'polls.productmodel': {
            'Meta': {'object_name': 'ProductModel'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'err_text': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idx': ('django.db.models.fields.IntegerField', [], {'default': "'Nil'", 'max_length': '10'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "'Nil'", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'Nil'", 'max_length': '10'}),
            'prod_url': ('django.db.models.fields.URLField', [], {'default': "'Nil'", 'max_length': '200'}),
            'promo_text': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'Nil'", 'max_length': '10'})
        },
        'polls.promoinfo': {
            'Meta': {'unique_together': "(('store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'),)", 'object_name': 'Promoinfo'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'd': ('django.db.models.fields.DateField', [], {}),
            'free_shipping_lower_bound': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_category': ('django.db.models.fields.IntegerField', [], {}),
            'promo_disc_amount': ('django.db.models.fields.IntegerField', [], {}),
            'promo_disc_lower_bound': ('django.db.models.fields.IntegerField', [], {}),
            'promo_disc_perc': ('django.db.models.fields.IntegerField', [], {}),
            'promo_type': ('django.db.models.fields.IntegerField', [], {}),
            'sex_category': ('django.db.models.fields.IntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'validity': ('django.db.models.fields.IntegerField', [], {}),
            'where_avail': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.resultfordemand': {
            'Meta': {'object_name': 'ResultForDemand'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 22, 7, 54, 32, 96514)'}),
            'demand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Demand']", 'null': 'True', 'blank': 'True'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_selection_metric': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'itemlist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.ItemList']", 'null': 'True', 'blank': 'True'}),
            'store_name': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']", 'null': 'True', 'blank': 'True'}),
            'store_string': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '10'}),
            'total_with_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'}),
            'total_without_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
        },
        'polls.ssitemstats': {
            'Meta': {'object_name': 'SSItemStats'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'-111.00'", 'max_length': '10'}),
            'price_selection_metric': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'sale_cnt': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'-111.00'", 'max_length': '10'}),
            'tdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 22, 7, 54, 32, 96999)'}),
            'total_cnt': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'})
        },
        'polls.storeitemcombinationresults': {
            'Meta': {'object_name': 'StoreItemCombinationResults'},
            'combination_id': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'Nil'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'Nil'", 'max_length': '10'})
        },
        'polls.wishlisti': {
            'Meta': {'object_name': 'WishlistI'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.ProductModel']", 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'default': "'-1111'", 'max_length': '50'})
        },
        'polls.wishlistm': {
            'Meta': {'object_name': 'WishlistM'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item1': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist1'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item10': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist10'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item11': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist11'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item12': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist12'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item13': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist13'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item14': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist14'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item15': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist15'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item16': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist16'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item2': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist2'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item3': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist3'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item4': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist4'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item5': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist5'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item6': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist6'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item7': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist7'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item8': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist8'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'item9': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'prodlist9'", 'null': 'True', 'blank': 'True', 'to': "orm['polls.ProductModel']"}),
            'total_prods': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        }
    }

    complete_apps = ['polls']