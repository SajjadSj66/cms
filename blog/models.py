from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=255)
    active = models.BooleanField(verbose_name=_("active"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Post(models.Model):

    class StatusChoices(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(verbose_name=_("title"), max_length=255)
    thumbnail = models.ImageField(verbose_name=_("thumb"), null=True, upload_to='posts/')
    slug = models.SlugField(verbose_name=_("slug"), allow_unicode=True, null=False, unique_for_date="publish_time")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    lead = models.CharField(verbose_name=_("Lead"), max_length=1024, null=True, blank=True)
    body = models.TextField(verbose_name=_("body"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("updated"), auto_now=True)

    status = models.CharField(verbose_name=_("status"), max_length=15, choices=StatusChoices.choices,
                              default=StatusChoices.DRAFT)
    featured = models.BooleanField(verbose_name=_("featured"), null=True)
    publish_time = models.DateTimeField(verbose_name=_("publish time"), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog:blog-item', args=[
            self.publish_time.year,
            self.publish_time.month,
            self.publish_time.day,
            self.slug
        ])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ["-publish_time"]

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("updated"), auto_now=True)
    approved = models.BooleanField()

    def __str__(self):
        return self.name

class SiteUser(AbstractUser):
    pass