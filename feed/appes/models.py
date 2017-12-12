import sys
import os
import time
from django.db.models import CharField, Model
from django.db import models
from django.urls.base import reverse
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField



#===============Myfeed==================#

# class Sublink(models.Model):
# 	blog_name = models.CharField(unique=True, db_index=True, default='', null=True, blank=True, max_length=255)

# 	def __unicode__(self):
# 		return str(self.blog_name)


class Myfeed(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True, default='')
    slug = AutoSlugField(unique=True, populate_from='title', null=True, blank=True)
    description = models.TextField( db_index=True, blank=True, null=True)
    category = models.CharField(max_length=255, null=True, db_index=True, blank=True)
    tag_id = models.CharField(max_length=255, blank=True, null=True, db_index=True, default='')

    main_link = models.URLField(db_index=True, default='')
    sub_link = models.URLField(unique=True, blank=True)
    published = models.CharField(max_length=255, blank=True, null=True, db_index=True, default='')
    updated = models.CharField(max_length=255, blank=True,null=True, db_index=True, default='')
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('myfeed',
                       kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title


class Addfeed(models.Model):
    url = models.URLField(db_index=True, unique=True, default='')

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('addfeed:feed_edit', kwargs={'pk': self.pk})        
