from django.db import models


class Theme(models.Model):
    short_name = models.CharField(max_length=200)
    name = models.TextField()


class City(models.Model):
    name = models.TextField()
    population = models.IntegerField()


class PoliceReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City)
    crimes_count = models.IntegerField()


class BlogsData(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(City)


class BlogEntry(models.Model):
    text = models.TextField()
    dataset = models.ForeignKey(BlogsData)
