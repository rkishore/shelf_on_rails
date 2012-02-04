# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Demand'
        db.create_table('polls_demand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_shirts', self.gf('django.db.models.fields.IntegerField')()),
            ('num_sweaters', self.gf('django.db.models.fields.IntegerField')()),
            ('num_skirts', self.gf('django.db.models.fields.IntegerField')()),
            ('num_jeans', self.gf('django.db.models.fields.IntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('total_items', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('polls', ['Demand'])

        # Adding model 'ResultForDemand'
        db.create_table('polls_resultfordemand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('demand', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', to=orm['polls.Demand'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 1, 11, 21, 23, 56, 775592))),
            ('itemlist', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', to=orm['polls.ItemList'])),
            ('total_without_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
            ('total_with_sale', self.gf('django.db.models.fields.FloatField')(default='10.00', max_length=10)),
            ('free_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('store_name', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', to=orm['polls.Brands'])),
            ('item_selection_metric', self.gf('django.db.models.fields.IntegerField')(default='0')),
        ))
        db.send_create_signal('polls', ['ResultForDemand'])

        # Adding model 'ItemList'
        db.create_table('polls_itemlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item1', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist1', to=orm['polls.Items'])),
            ('item2', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist2', to=orm['polls.Items'])),
            ('item3', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist3', to=orm['polls.Items'])),
            ('item4', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist4', to=orm['polls.Items'])),
            ('item5', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist5', to=orm['polls.Items'])),
            ('item6', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist6', to=orm['polls.Items'])),
            ('item7', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist7', to=orm['polls.Items'])),
            ('item8', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist8', to=orm['polls.Items'])),
            ('item9', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist9', to=orm['polls.Items'])),
            ('item10', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist10', to=orm['polls.Items'])),
            ('item11', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist11', to=orm['polls.Items'])),
            ('item12', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist12', to=orm['polls.Items'])),
            ('item13', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist13', to=orm['polls.Items'])),
            ('item14', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist14', to=orm['polls.Items'])),
            ('item15', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist15', to=orm['polls.Items'])),
            ('item16', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', related_name='itemlist16', to=orm['polls.Items'])),
            ('total_items', self.gf('django.db.models.fields.IntegerField')(default='0')),
        ))
        db.send_create_signal('polls', ['ItemList'])


    def backwards(self, orm):
        
        # Deleting model 'Demand'
        db.delete_table('polls_demand')

        # Deleting model 'ResultForDemand'
        db.delete_table('polls_resultfordemand')

        # Deleting model 'ItemList'
        db.delete_table('polls_itemlist')


    models = {
        'polls.brands': {
            'Meta': {'object_name': 'Brands'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'})
        },
        'polls.categories': {
            'Meta': {'object_name': 'Categories'},
            'brand': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['polls.Brands']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '100'})
        },
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
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
            'item1': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist1'", 'to': "orm['polls.Items']"}),
            'item10': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist10'", 'to': "orm['polls.Items']"}),
            'item11': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist11'", 'to': "orm['polls.Items']"}),
            'item12': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist12'", 'to': "orm['polls.Items']"}),
            'item13': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist13'", 'to': "orm['polls.Items']"}),
            'item14': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist14'", 'to': "orm['polls.Items']"}),
            'item15': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist15'", 'to': "orm['polls.Items']"}),
            'item16': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist16'", 'to': "orm['polls.Items']"}),
            'item2': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist2'", 'to': "orm['polls.Items']"}),
            'item3': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist3'", 'to': "orm['polls.Items']"}),
            'item4': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist4'", 'to': "orm['polls.Items']"}),
            'item5': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist5'", 'to': "orm['polls.Items']"}),
            'item6': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist6'", 'to': "orm['polls.Items']"}),
            'item7': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist7'", 'to': "orm['polls.Items']"}),
            'item8': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist8'", 'to': "orm['polls.Items']"}),
            'item9': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'related_name': "'itemlist9'", 'to': "orm['polls.Items']"}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 1, 11, 21, 23, 56, 775592)'}),
            'demand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Demand']"}),
            'free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_selection_metric': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'itemlist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.ItemList']"}),
            'store_name': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'total_with_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'}),
            'total_without_sale': ('django.db.models.fields.FloatField', [], {'default': "'10.00'", 'max_length': '10'})
        },
        'polls.wishlistm': {
            'Meta': {'object_name': 'WishlistM'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['polls']
