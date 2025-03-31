import time
from datetime import datetime

import feedparser

from news_monitoring.story import models as story_models

def import_stories_from_feed(source, user):
    """
    Parse the RSS feed from the source URL and create Story objects for each feed entry.
    Only creates stories that don't already exist based on article_url.
    """
    feed = feedparser.parse(source.url)
    for entry in feed.entries:
        # Avoid duplicate story creation based on article_url
        if not story_models.Story.objects.filter(article_url=entry.link).exists():
            # Try to extract a published date if available
            published_date = None
            if hasattr(entry, 'published_parsed'):
                published_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            # Use summary if available; otherwise, you can check for 'content'
            body_text = entry.get('summary', '')

            # Create the story object
            story_models.Story.objects.create(
                title=entry.title,
                body_text=body_text,
                article_url=entry.link,
                published_date=published_date,
                company=source.company,  # You might want to set company from the source or current user context
                source=source,
                added_by=user
            )
