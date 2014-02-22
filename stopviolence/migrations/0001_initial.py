# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table(u'stopviolence_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'stopviolence', ['Theme'])

        # Adding model 'City'
        db.create_table(u'stopviolence_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stopviolence', ['City'])

        # Adding model 'PoliceReport'
        db.create_table(u'stopviolence_policereport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stopviolence.City'])),
            ('crimes_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'stopviolence', ['PoliceReport'])

        # Adding model 'BlogsData'
        db.create_table(u'stopviolence_blogsdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stopviolence.City'])),
        ))
        db.send_create_signal(u'stopviolence', ['BlogsData'])

        # Adding model 'BlogEntry'
        db.create_table(u'stopviolence_blogentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stopviolence.BlogsData'])),
        ))
        db.send_create_signal(u'stopviolence', ['BlogEntry'])


    def backwards(self, orm):
        # Deleting model 'Theme'
        db.delete_table(u'stopviolence_theme')

        # Deleting model 'City'
        db.delete_table(u'stopviolence_city')

        # Deleting model 'PoliceReport'
        db.delete_table(u'stopviolence_policereport')

        # Deleting model 'BlogsData'
        db.delete_table(u'stopviolence_blogsdata')

        # Deleting model 'BlogEntry'
        db.delete_table(u'stopviolence_blogentry')


    models = {
        u'stopviolence.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stopviolence.BlogsData']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'stopviolence.blogsdata': {
            'Meta': {'object_name': 'BlogsData'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stopviolence.City']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'stopviolence.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'population': ('django.db.models.fields.IntegerField', [], {})
        },
        u'stopviolence.policereport': {
            'Meta': {'object_name': 'PoliceReport'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stopviolence.City']"}),
            'crimes_count': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'stopviolence.theme': {
            'Meta': {'object_name': 'Theme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['stopviolence']