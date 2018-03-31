# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils import timezone
from slugify import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import re


def random_string(n):
    import random
    import string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def upload_image_path_handler(instance, filename):
    ext = filename.split('.')[-1]
    name = slugify(filename)
    return "images/{name}_{random}.{ext}".format(random=random_string(8), name=name, ext=ext)


class Community(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    create_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


class Act(models.Model):
    name = models.CharField(max_length=100)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=100, blank=True)
    preview = RichTextField()
    create_date = models.DateTimeField(default=timezone.now())
    image = models.ImageField(upload_to=upload_image_path_handler, blank=True, null=True)

    def __str__(self):
        return self.name


class Critic(models.Model):
    editor = models.ForeignKey('auth.user')
    act = models.ForeignKey(Act, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextField()
    pub_date = models.DateTimeField(default=timezone.now())
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.title

    def get_short_text(self):
        first_sub = re.sub('<[^<]+?>', '', self.text)
        if len(self.text) > 200:
            return re.sub('&nbsp;', '', first_sub[:200]+'...')
        else:
            return re.sub('&nbsp;', '', first_sub)

    def get_long_text(self):
        first_sub = re.sub('<[^<]+?>', '', self.text)
        if len(self.text) > 400:
            return re.sub('&nbsp;', '', first_sub[:400]+'...')
        else:
            return re.sub('&nbsp;', '', first_sub)

    def get_twt_text(self):
        first_sub = re.sub('<[^<]+?>', '', self.title + ' - ' + self.text)
        if len(self.text) > 140:
            return re.sub('&nbsp;', '', first_sub[:137]+'...')
        else:
            return re.sub('&nbsp;', '', first_sub)

    def get_pub_date(self):
        return self.pub_date.date()


class Comment(models.Model):
    critic = models.ForeignKey(Critic, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now())
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.text
