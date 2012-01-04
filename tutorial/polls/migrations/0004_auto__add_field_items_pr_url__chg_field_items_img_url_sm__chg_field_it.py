# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Items.pr_url'
        db.add_column('polls_items', 'pr_url', self.gf('django.db.models.fields.CharField')(default='Nil', max_length=200), keep_default=False)

        # Changing field 'Items.img_url_sm'
        db.alter_column('polls_items', 'img_url_sm', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Items.img_url_md'
        db.alter_column('polls_items', 'img_url_md', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Items.img_url_lg'
        db.alter_column('polls_items', 'img_url_lg', self.gf('django.db.models.fields.CharField')(max_length=200))


    def backwards(self, orm):
        
        # Deleting field 'Items.pr_url'
        db.delete_column('polls_items', 'pr_url')

        # Changing field 'Items.img_url_sm'
        db.alter_column('polls_items', 'img_url_sm', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Items.img_url_md'
        db.alter_column('polls_items', 'img_url_md', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Items.img_url_lg'
        db.alter_column('polls_items', 'img_url_lg', self.gf('django.db.models.fields.CharField')(max_length=100))


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
            'img_url_lg': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'img_url_md': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'img_url_sm': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'insert_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
            'pr_url': ('django.db.models.fields.CharField', [], {'default': "'Nil'", 'max_length': '200'}),
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
            'store': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Nil'", 'to': "orm['polls.Brands']"}),
            'validity': ('django.db.models.fields.IntegerField', [], {}),
            'where_avail': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['polls']
