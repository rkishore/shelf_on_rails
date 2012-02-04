# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Poll'
        db.create_table('polls_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('polls', ['Poll'])

        # Adding model 'Choice'
        db.create_table('polls_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('polls', ['Choice'])

        # Adding model 'Promoinfo'
        db.create_table('polls_promoinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('d', self.gf('django.db.models.fields.DateField')()),
            ('validity', self.gf('django.db.models.fields.IntegerField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('where_avail', self.gf('django.db.models.fields.IntegerField')()),
            ('free_shipping_lower_bound', self.gf('django.db.models.fields.IntegerField')()),
            ('promo_type', self.gf('django.db.models.fields.IntegerField')()),
            ('promo_disc_perc', self.gf('django.db.models.fields.IntegerField')()),
            ('promo_disc_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('promo_disc_lower_bound', self.gf('django.db.models.fields.IntegerField')()),
            ('sex_category', self.gf('django.db.models.fields.IntegerField')()),
            ('item_category', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('polls', ['Promoinfo'])

        # Adding unique constraint on 'Promoinfo', fields ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category']
        db.create_unique('polls_promoinfo', ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'])

        # Adding model 'Brands'
        db.create_table('polls_brands', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
        ))
        db.send_create_signal('polls', ['Brands'])

        # Adding model 'Items'
        db.create_table('polls_items', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='Nil', to=orm['polls.Brands'])),
            ('gender', self.gf('django.db.models.fields.CharField')(default='A', max_length=6)),
            ('cat1', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat2', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat3', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat4', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('cat5', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200)),
            ('price', self.gf('django.db.models.fields.CharField')(default='20.00', max_length=10)),
            ('saleprice', self.gf('django.db.models.fields.CharField')(default='10.00', max_length=10)),
            ('insert_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('polls', ['Items'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Promoinfo', fields ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category']
        db.delete_unique('polls_promoinfo', ['store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount', 'promo_disc_lower_bound', 'sex_category', 'item_category'])

        # Deleting model 'Poll'
        db.delete_table('polls_poll')

        # Deleting model 'Choice'
        db.delete_table('polls_choice')

        # Deleting model 'Promoinfo'
        db.delete_table('polls_promoinfo')

        # Deleting model 'Brands'
        db.delete_table('polls_brands')

        # Deleting model 'Items'
        db.delete_table('polls_items')


    models = {
        'polls.brands': {
            'Meta': {'object_name': 'Brands'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'})
        },
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
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
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'price': ('django.db.models.fields.CharField', [], {'default': "'20.00'", 'max_length': '10'}),
            'saleprice': ('django.db.models.fields.CharField', [], {'default': "'10.00'", 'max_length': '10'})
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
            'store': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'validity': ('django.db.models.fields.IntegerField', [], {}),
            'where_avail': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['polls']
