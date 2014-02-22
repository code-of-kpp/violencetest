import feedparser
import requests
import logging


from .models import BlogsData, BlogEntry


logger = logging.get_logger(__name__)


def process_police_report(report):

    processed = 0
    finished = False
    page = None

    blogs_data = BlogsData(city=report.city,
                           start_date=report.start_date,
                           end_date=report.end_date)
    blogs_data.save()

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
                                   text=text)
            blog_entry.save()

        processed += len(posts.entries)

        finished = (len(posts.entries) == 0) or (posts.feed.yablogs_count <= processed)
        page = page + 1 if page else 2
        logger.debug(page, processed, posts.feed.yablogs_count)
