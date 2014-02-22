from django.db import models
from django.utils.translation import ugettext_lazy as _


class Theme(models.Model):
    short_name = models.CharField(max_length=200)
    name = models.TextField()

    class Meta:
        verbose_name = _("Theme")

    def __unicode__(self):
        return self.name


class ViolentPhoto(models.Model):
    theme = models.ForeignKey(Theme)
    short_name = models.CharField(max_length=200)
    phnto_link = models.URLField(unique=True)
    news_link = models.URLField()
    violent_level = models.FloatField()

    def __unicode__(self):
        return self.short_name


class City(models.Model):
    name = models.TextField(unique=True)
    population = models.IntegerField()

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __unicode__(self):
        return self.name


class PoliceReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City)
    crimes_count = models.IntegerField()

    def __unicode__(self):
        return '{} crimes at {}'.format(self.crimes, self.city.name)


class BlogsData(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City)

    class Meta:
        verbose_name = _("Blogs data")
        verbose_name_plural = _("Blogs data collections")

    def __unicode__(self):
        return u'{} {}--{}'.format(self.city.name, self.start_date, self.end_date)


class BlogEntry(models.Model):
    text = models.TextField()
    dataset = models.ForeignKey(BlogsData)

    class Meta:
        verbose_name = _("Blog entry")
        verbose_name_plural = _("Blog entries")

    def __unicode__(self):
        return self.text

    def __repr__(self):
        return super(BlogEntry, self).__repr__()[:45]


class UserResult(models.Model):
    link = models.URLField()
    level = models.FloatField()
