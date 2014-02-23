from django.db import models
from django.utils.translation import ugettext_lazy as _

from scipy import sparse

from cqlwrapper import cqlmodels


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
        return u'{} crimes at {}'.format(self.crimes_count, self.city.name)


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
    raw = models.TextField(null=True)

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


class Ngram(models.Model):
    string = models.TextField(db_index=True)


class ClassCounters(cqlmodels.Model):
    class_ = cqlmodels.Integer(primary_key=True)  # 0 for all
    value = cqlmodels.Counter()


class NgramCounters(cqlmodels.Model):
    class_ = cqlmodels.Integer(primary_key=True)  # 0 for all
    ngram = cqlmodels.Integer(primary_key=True)
    value = cqlmodels.Counter()


def add_ngram(terms, dataset_id):
    string = ' '.join(terms)
    ngram, _ = Ngram.objects.get_or_create(string=string)

    cc = ClassCounters()
    cc.class_ = dataset_id
    cc.value = 1
    cc.save()

    cc0 = ClassCounters()
    cc0.class_ = 0
    cc0.value = 1
    cc0.save()

    nc = NgramCounters()
    nc.class_ = dataset_id
    nc.ngram = ngram.pk
    nc.value = 1
    nc.save()

    nc0 = NgramCounters()
    nc0.class_ = 0
    nc0.ngram = ngram.pk
    nc0.value = 1
    nc0.save()


def get_train_data():
    rows = PoliceReport.objects.count()
    cols = Ngram.objects.last().pk

    data = sparce.dok_matrix((rows, cols))

    all_ngram_counters = NgramCounters.objects.filter(class_=0)

    levels = list()

    for row, pr in enumerated(PoliceReport.objects):
        g = NgramCounters.objects.filter(class_=pr.pk).all()
        for nc in g:
            data[(row, nc.ngram)] = float(nc.value) / all_ngram_counters.get(ngram=nc.ngram).value
        levels.append(float(pr.crimes_count) / pr.city.population / (pr.end_date - pr.start_date).days)

    return data, levels
