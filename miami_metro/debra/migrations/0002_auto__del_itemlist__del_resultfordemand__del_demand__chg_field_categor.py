# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ItemList'
        db.delete_table('debra_itemlist')

        # Deleting model 'ResultForDemand'
        db.delete_table('debra_resultfordemand')

        # Deleting model 'Demand'
        db.delete_table('debra_demand')

        # Changing field 'CategoryModel.categoryName'
        db.alter_column('debra_categorymodel', 'categoryName', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Adding field 'ProductModel.description'
        db.add_column('debra_productmodel', 'description', self.gf('django.db.models.fields.TextField')(default='Nil'), keep_default=False)

        # Adding field 'Items.product_model_key'
        db.add_column('debra_items', 'product_model_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['debra.ProductModel'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'ItemList'
        db.create_table('debra_itemlist', (
            ('total_items', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('item8', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist8', null=True, to=orm['debra.Items'], blank=True)),
            ('item9', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist9', null=True, to=orm['debra.Items'], blank=True)),
            ('item2', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist2', null=True, to=orm['debra.Items'], blank=True)),
            ('item3', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist3', null=True, to=orm['debra.Items'], blank=True)),
            ('item1', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist1', null=True, to=orm['debra.Items'], blank=True)),
            ('item6', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist6', null=True, to=orm['debra.Items'], blank=True)),
            ('item7', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist7', null=True, to=orm['debra.Items'], blank=True)),
            ('item4', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist4', null=True, to=orm['debra.Items'], blank=True)),
            ('item11', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist11', null=True, to=orm['debra.Items'], blank=True)),
            ('item14', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist14', null=True, to=orm['debra.Items'], blank=True)),
            ('item15', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist15', null=True, to=orm['debra.Items'], blank=True)),
            ('item16', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist16', null=True, to=orm['debra.Items'], blank=True)),
            ('item5', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist5', null=True, to=orm['debra.Items'], blank=True)),
            ('item10', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist10', null=True, to=orm['debra.Items'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item12', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist12', null=True, to=orm['debra.Items'], blank=True)),
            ('item13', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist13', null=True, to=orm['debra.Items'], blank=True)),
        ))
        db.send_create_signal('debra', ['ItemList'])

        # Adding model 'ResultForDemand'
        db.create_table('debra_resultfordemand', (
            ('total_without_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
            ('item_selection_metric', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('itemlist', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.ItemList'], null=True, blank=True)),
            ('demand', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.Demand'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 1, 28, 14, 54, 5, 531800))),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_with_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
            ('free_shipping', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('store_string', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=20)),
            ('store_name', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'], null=True, blank=True)),
        ))
        db.send_create_signal('debra', ['ResultForDemand'])

        # Adding model 'Demand'
        db.create_table('debra_demand', (
            ('total_items', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_shirts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_skirts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('num_sweaters', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_jeans', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('debra', ['Demand'])

        # Changing field 'CategoryModel.categoryName'
        db.alter_column('debra_categorymodel', 'categoryName', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Deleting field 'ProductModel.description'
        db.delete_column('debra_productmodel', 'description')

        # Deleting field 'Items.product_model_key'
        db.delete_column('debra_items', 'product_model_key_id')


    models = {
        'debra.brands': {
            'Meta': {'object_name': 'Brands'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'})
        },
        'debra.categories': {
            'Meta': {'object_name': 'Categories'},
            'brand': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['debra.Brands']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'})
        },
        'debra.categorymodel': {
            'Meta': {'object_name': 'CategoryModel'},
            'categoryId': ('django.db.models.fields.IntegerField', [], {'default': "'-111'", 'max_length': '50'}),
            'categoryName': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.ProductModel']"})
        },
        'debra.colorsizemodel': {
            'Meta': {'object_name': 'ColorSizeModel'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.ProductModel']"}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'})
        },
        'debra.items': {
            'Meta': {'object_name': 'Items'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']"}),
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
            'pr_colors': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '600'}),
            'pr_currency': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_instock': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '10'}),
            'pr_retailer': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_sizes': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '600'}),
            'pr_url': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'20.00'", 'max_length': '10'}),
            'product_model_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['debra.ProductModel']", 'null': 'True', 'blank': 'True'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
        },
        'debra.productmodel': {
            'Meta': {'object_name': 'ProductModel'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'Nil'"}),
            'err_text': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idx': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'}),
            'img_url': ('django.db.models.fields.URLField', [], {'default': "'Nil'", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'-11.0'", 'max_length': '10'}),
            'prod_url': ('django.db.models.fields.URLField', [], {'default': "'Nil'", 'max_length': '200'}),
            'promo_text': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'-11.0'", 'max_length': '10'})
        },
        'debra.promoinfo': {
            'Meta': {'unique_together': "(('store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'),)", 'object_name': 'Promoinfo'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'd': ('django.db.models.fields.DateField', [], {}),
            'free_shipping_lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_category': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'promo_disc_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'promo_disc_lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'promo_disc_perc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'promo_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sex_category': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']"}),
            'validity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'where_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'debra.ssitemstats': {
            'Meta': {'object_name': 'SSItemStats'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'-111.00'", 'max_length': '10'}),
            'price_selection_metric': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale_cnt': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'-111.00'", 'max_length': '10'}),
            'tdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 30, 16, 39, 41, 520116)'}),
            'total_cnt': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'})
        },
        'debra.storeitemcombinationresults': {
            'Meta': {'object_name': 'StoreItemCombinationResults'},
            'combination_id': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': "'-11.0'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'-11.0'", 'max_length': '10'})
        },
        'debra.useridmap': {
            'Meta': {'object_name': 'UserIdMap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.CharField', [], {'default': "'-11.11.11.11'", 'max_length': '50'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'default': "'-1111'", 'max_length': '50'})
        },
        'debra.wishlisti': {
            'Meta': {'object_name': 'WishlistI'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.ProductModel']", 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.UserIdMap']"})
        }
    }

    complete_apps = ['debra']
