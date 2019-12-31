# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserDashboardModule'
        db.create_table(u'dashboard_userdashboardmodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('column', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('settings', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('children', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('collapsed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'dashboard', ['UserDashboardModule'])


    def backwards(self, orm):
        # Deleting model 'UserDashboardModule'
        db.delete_table(u'dashboard_userdashboardmodule')


    models = {
        u'dashboard.userdashboardmodule': {
            'Meta': {'ordering': "('column', 'order')", 'object_name': 'UserDashboardModule'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'children': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'collapsed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'column': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'settings': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['dashboard']