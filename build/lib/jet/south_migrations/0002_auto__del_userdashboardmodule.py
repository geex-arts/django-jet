# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserDashboardModule'
        db.delete_table(u'jet_userdashboardmodule')


    def backwards(self, orm):
        # Adding model 'UserDashboardModule'
        db.create_table(u'jet_userdashboardmodule', (
            ('collapsed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('children', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('column', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('settings', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'jet', ['UserDashboardModule'])


    models = {
        u'jet.bookmark': {
            'Meta': {'ordering': "('date_add',)", 'object_name': 'Bookmark'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'jet.pinnedapplication': {
            'Meta': {'ordering': "('date_add',)", 'object_name': 'PinnedApplication'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['jet']