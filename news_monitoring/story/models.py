from django.db import models

from news_monitoring.users import models as user_models
from news_monitoring.source import models as source_models

# Story Model
class Story(models.Model):
    tagged_company = models.ManyToManyField(user_models.Company, related_name='tagged_stories', blank=True)

    company = models.ForeignKey(user_models.Company, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(source_models.Source, on_delete=models.SET_NULL, null=True, blank=True)
    added_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='stories_added')
    updated_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='stories_updated', null=True, blank=True)

    title = models.CharField(max_length=255, null=False, blank=False)
    body_text = models.TextField(null=False, blank=False)
    article_url = models.URLField(null=False, blank=False)

    published_date = models.DateTimeField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Unique constraint to ensure the combination of company_id and article_url is unique
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['company', 'article_url'], name='unique_company_article_url')
        ]

    def __str__(self):
        return f"{self.title} ({self.company.name if self.company else 'No Company'})"
