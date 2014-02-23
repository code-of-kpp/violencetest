import feedparser
import requests
import logging


from .models import BlogsData, BlogEntry


logger = logging.getLogger(__name__)


def process_police_report(report):

    processed = 0
    finished = False
    page = None

    blogs_data = BlogsData(pk=report.pk,
                           city=report.city,
                           start_date=report.start_date,
                           end_date=report.end_date)
    blogs_data.save()

    try:
        BlogEntry.objects.filter(dataset=blogs_data.pk).delete()
    except BlogEntry.DoesNotExist:
        pass

    while not finished:
        response = requests.get('http://blogs.yandex.ru/search.rss',
             params={'geo': report.city.name,
                     'from_day': report.start_date.day,
                     'from_month': report.start_date.month,
                     'from_year': report.start_date.year,
                     'to_day': report.end_date.day,
                     'to_month': report.end_date.month,
                     'to_year': report.end_date.year,
                     'ft': 'all',
                     'numdoc': 100,
                     'p': page})
        posts = feedparser.parse(response.text)

        for post in posts.entries:
            text = post.description if (post.title in post.description) else (post.title + post.description)

            blog_entry = BlogEntry(dataset_id=blogs_data.pk,
                                   text=text, raw=unicode(post))
            blog_entry.save()

        processed += len(posts.entries)

        finished = (len(posts.entries) == 0) or (posts.feed.yablogs_count <= processed)
        page = page + 1 if page else 1
        logger.debug(page, processed, getattr(posts.feed, 'yablogs_count', ''))

    return blogs_data
