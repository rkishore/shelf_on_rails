# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Promoinfo'
        db.create_table('debra_promoinfo', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('d', self.gf('django.db.models.fields.DateField')()),
            ('where_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('promo_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('free_shipping_lower_bound', self.gf('django.db.models.fields.IntegerField')(default=10000)),
            ('validity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('promo_disc_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('promo_disc_lower_bound', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex_category', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('promo_disc_perc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'])),
            ('item_category', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('debra', ['Promoinfo'])

        # Adding unique constraint on 'Promoinfo', fields ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category']
        db.create_unique('debra_promoinfo', ['store_id', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'])

        # Adding model 'Brands'
        db.create_table('debra_brands', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
        ))
        db.send_create_signal('debra', ['Brands'])

        # Adding model 'Items'
        db.create_table('debra_items', (
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('pr_colors', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=600)),
            ('pr_retailer', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('pr_currency', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('pr_sizes', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=600)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'])),
            ('img_url_sm', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('pr_url', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('price', self.gf('django.db.models.fields.FloatField')(default='20.00', max_length=10)),
            ('cat1', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat2', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat3', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat4', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat5', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('img_url_lg', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('pr_instock', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=10)),
            ('img_url_md', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('saleprice', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
        ))
        db.send_create_signal('debra', ['Items'])

        # Adding model 'Categories'
        db.create_table('debra_categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
        ))
        db.send_create_signal('debra', ['Categories'])

        # Adding M2M table for field brand on 'Categories'
        db.create_table('debra_categories_brand', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('categories', models.ForeignKey(orm['debra.categories'], null=False)),
            ('brands', models.ForeignKey(orm['debra.brands'], null=False))
        ))
        db.create_unique('debra_categories_brand', ['categories_id', 'brands_id'])

        # Adding model 'Demand'
        db.create_table('debra_demand', (
            ('total_items', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('num_jeans', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_shirts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_skirts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_sweaters', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('debra', ['Demand'])

        # Adding model 'ItemList'
        db.create_table('debra_itemlist', (
            ('total_items', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('item8', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist8', null=True, blank=True, to=orm['debra.Items'])),
            ('item9', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist9', null=True, blank=True, to=orm['debra.Items'])),
            ('item2', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist2', null=True, blank=True, to=orm['debra.Items'])),
            ('item3', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist3', null=True, blank=True, to=orm['debra.Items'])),
            ('item1', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist1', null=True, blank=True, to=orm['debra.Items'])),
            ('item6', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist6', null=True, blank=True, to=orm['debra.Items'])),
            ('item7', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist7', null=True, blank=True, to=orm['debra.Items'])),
            ('item4', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist4', null=True, blank=True, to=orm['debra.Items'])),
            ('item5', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist5', null=True, blank=True, to=orm['debra.Items'])),
            ('item15', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist15', null=True, blank=True, to=orm['debra.Items'])),
            ('item14', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist14', null=True, blank=True, to=orm['debra.Items'])),
            ('item11', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist11', null=True, blank=True, to=orm['debra.Items'])),
            ('item16', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist16', null=True, blank=True, to=orm['debra.Items'])),
            ('item10', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist10', null=True, blank=True, to=orm['debra.Items'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item12', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist12', null=True, blank=True, to=orm['debra.Items'])),
            ('item13', self.gf('django.db.models.fields.related.ForeignKey')(default='0', related_name='itemlist13', null=True, blank=True, to=orm['debra.Items'])),
        ))
        db.send_create_signal('debra', ['ItemList'])

        # Adding model 'ResultForDemand'
        db.create_table('debra_resultfordemand', (
            ('free_shipping', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('total_without_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
            ('store_string', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=20)),
            ('item_selection_metric', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('store_name', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'], null=True, blank=True)),
            ('itemlist', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.ItemList'], null=True, blank=True)),
            ('demand', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.Demand'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 1, 28, 14, 54, 5, 531800))),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_with_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
        ))
        db.send_create_signal('debra', ['ResultForDemand'])

        # Adding model 'SSItemStats'
        db.create_table('debra_ssitemstats', (
            ('category', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=10)),
            ('total_cnt', self.gf('django.db.models.fields.IntegerField')(default='-11', max_length=10)),
            ('price_selection_metric', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'])),
            ('tdate', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 1, 28, 14, 54, 5, 532760))),
            ('price', self.gf('django.db.models.fields.FloatField')(default='-111.00', max_length=10)),
            ('saleprice', self.gf('django.db.models.fields.FloatField')(default='-111.00', max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sale_cnt', self.gf('django.db.models.fields.IntegerField')(default='-11', max_length=10)),
        ))
        db.send_create_signal('debra', ['SSItemStats'])

        # Adding model 'ProductModel'
        db.create_table('debra_productmodel', (
            ('err_text', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('prod_url', self.gf('django.db.models.fields.URLField')(default='Nil', max_length=200)),
            ('idx', self.gf('django.db.models.fields.IntegerField')(default='-11', max_length=10)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=6)),
            ('price', self.gf('django.db.models.fields.FloatField')(default='-11.0', max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('saleprice', self.gf('django.db.models.fields.FloatField')(default='-11.0', max_length=10)),
            ('promo_text', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('img_url', self.gf('django.db.models.fields.URLField')(default='Nil', max_length=200)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='1', to=orm['debra.Brands'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
        ))
        db.send_create_signal('debra', ['ProductModel'])

        # Adding model 'ColorSizeModel'
        db.create_table('debra_colorsizemodel', (
            ('color', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=50)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.ProductModel'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=50)),
        ))
        db.send_create_signal('debra', ['ColorSizeModel'])

        # Adding model 'CategoryModel'
        db.create_table('debra_categorymodel', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.ProductModel'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoryName', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=50)),
            ('categoryId', self.gf('django.db.models.fields.IntegerField')(default='-111', max_length=50)),
        ))
        db.send_create_signal('debra', ['CategoryModel'])

        # Adding model 'UserIdMap'
        db.create_table('debra_useridmap', (
            ('user_id', self.gf('django.db.models.fields.IntegerField')(default='-1111', max_length=50)),
            ('ip_addr', self.gf('django.db.models.fields.CharField')(default='-11.11.11.11', max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('debra', ['UserIdMap'])

        # Adding model 'WishlistI'
        db.create_table('debra_wishlisti', (
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.ProductModel'], null=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(default='0', to=orm['debra.UserIdMap'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('debra', ['WishlistI'])

        # Adding model 'StoreItemCombinationResults'
        db.create_table('debra_storeitemcombinationresults', (
            ('combination_id', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('price', self.gf('django.db.models.fields.FloatField')(default='-11.0', max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('free_shipping', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('saleprice', self.gf('django.db.models.fields.FloatField')(default='-11.0', max_length=10)),
        ))
        db.send_create_signal('debra', ['StoreItemCombinationResults'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Promoinfo'
        db.delete_table('debra_promoinfo')

        # Removing unique constraint on 'Promoinfo', fields ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category']
        db.delete_unique('debra_promoinfo', ['store_id', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'])

        # Deleting model 'Brands'
        db.delete_table('debra_brands')

        # Deleting model 'Items'
        db.delete_table('debra_items')

        # Deleting model 'Categories'
        db.delete_table('debra_categories')

        # Removing M2M table for field brand on 'Categories'
        db.delete_table('debra_categories_brand')

        # Deleting model 'Demand'
        db.delete_table('debra_demand')

        # Deleting model 'ItemList'
        db.delete_table('debra_itemlist')

        # Deleting model 'ResultForDemand'
        db.delete_table('debra_resultfordemand')

        # Deleting model 'SSItemStats'
        db.delete_table('debra_ssitemstats')

        # Deleting model 'ProductModel'
        db.delete_table('debra_productmodel')

        # Deleting model 'ColorSizeModel'
        db.delete_table('debra_colorsizemodel')

        # Deleting model 'CategoryModel'
        db.delete_table('debra_categorymodel')

        # Deleting model 'UserIdMap'
        db.delete_table('debra_useridmap')

        # Deleting model 'WishlistI'
        db.delete_table('debra_wishlisti')

        # Deleting model 'StoreItemCombinationResults'
        db.delete_table('debra_storeitemcombinationresults')
    
    
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
            'categoryName': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '50'}),
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
        'debra.demand': {
            'Meta': {'object_name': 'Demand'},
            'gender': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_jeans': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_shirts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_skirts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_sweaters': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_items': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'debra.itemlist': {
            'Meta': {'object_name': 'ItemList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item1': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist1'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item10': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist10'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item11': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist11'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item12': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist12'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item13': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist13'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item14': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist14'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item15': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist15'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item16': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist16'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item2': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist2'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item3': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist3'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item4': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist4'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item5': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist5'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item6': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist6'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item7': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist7'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item8': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist8'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'item9': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'related_name': "'itemlist9'", 'null': 'True', 'blank': 'True', 'to': "orm['debra.Items']"}),
            'total_items': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'saleprice': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
        },
        'debra.productmodel': {
            'Meta': {'object_name': 'ProductModel'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']"}),
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
        'debra.resultfordemand': {
            'Meta': {'object_name': 'ResultForDemand'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 28, 14, 54, 5, 531800)'}),
            'demand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.Demand']", 'null': 'True', 'blank': 'True'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_selection_metric': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'itemlist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'0'", 'to': "orm['debra.ItemList']", 'null': 'True', 'blank': 'True'}),
            'store_name': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['debra.Brands']", 'null': 'True', 'blank': 'True'}),
            'store_string': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '20'}),
            'total_with_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'}),
            'total_without_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
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
            'tdate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 28, 14, 54, 5, 532760)'}),
            'total_cnt': ('django.db.models.fields.IntegerField', [], {'default': "'-11'", 'max_length': '10'})
        },
        'debra.storeitemcombinationresults': {
            'Meta': {'object_name': 'StoreItemCombinationResults'},
            'combination_id': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
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
