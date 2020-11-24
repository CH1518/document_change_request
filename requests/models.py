from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()


# class Area(models.Model):
#     area = models.CharField(max_length=255,unique=True)
#
#     def __str__(self):
#         return self.area

STATUS_CHOICES = (
    ('New - Pending Review','New - Pending Review'),
    ('In Progress', 'In Progress'),
    ('Reject','Reject'),
    ('Closed','Closed'),
)

NEW = (
    ('Select','Select'),
    ('Yes','Yes'),
    ('No', 'No'),
)

PRIORITY = (
    ('Select','Select'),
    ('High','High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
)

AREA = (
    ('Select','Select'),
    ('Admin','Admin'),
    ('Asset Prep', 'Asset Prep'),
    ('Box/Stow','Box/Stow'),
    ('QA','QA'),
    ('Receiving','Receiving'),
    ('Refurb','Refurb'),
    ('Registration','Registration'),
    ('Repair','Repair'),
    ('Shipping','Shipping'),
    ('Test','Test'),
)

class Request(models.Model):
    user = models.ForeignKey(User, related_name='request',on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    document_title = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    priority = models.CharField(max_length=20, choices=PRIORITY, default=' ')
    new_document_or_process = models.CharField(max_length=20, choices=NEW, default=' ')
    are_other_stakeholders_affected = models.CharField(max_length=20, choices=NEW, default=' ')
    requested_changes = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    area = models.CharField(max_length=20, choices=AREA, default=' ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New - Pending Review')
    revision_number = models.CharField(max_length=3,default=' ',unique=False)
    reason_for_change = models.TextField(blank=True,default='')
    file_name = models.CharField(max_length=255,unique=False)
    file = models.CharField(max_length=255,unique=False)

    def __str__(self):
        return self.document_title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.document_title)
        self.description_html = misaka.html(self.requested_changes)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('requests:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Request,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(User, related_name='comment',on_delete=models.CASCADE, null=True, default='.')
    email = models.EmailField(null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('requests:single',kwargs={'username':self.user.username,'slug':self.slug})

    class Meta:
        ordering = ['-created_on']
        # unique_together = ['name','body']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
