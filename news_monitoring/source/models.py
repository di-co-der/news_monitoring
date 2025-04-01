from django.db import models
from django.db.models import Q

from news_monitoring.users import models as user_models

# Source Model
class Source(models.Model):
   tagged_company = models.ManyToManyField(user_models.Company, related_name='tagged_sources', blank=True)

   company = models.ForeignKey(user_models.Company, on_delete=models.CASCADE, null=True,blank=True)
   added_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='sources_added', default=1)
   updated_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='sources_updated', null=True, blank=True)

   name = models.CharField(max_length=255)
   url = models.URLField(unique=True, null=False, blank=False, max_length=500)
   added_on = models.DateTimeField(auto_now_add=True)
   updated_on = models.DateTimeField(auto_now=True)

   # Unique constraint to ensure that company_id and url combination is unique
   class Meta:
       constraints = [
           models.UniqueConstraint(fields=['company', 'url'], name='unique_company_url'),

           # Check constraint to ensure URL starts with "http" or "https"
           models.CheckConstraint(
               check=Q(url__startswith="http"),
               name="check_valid_url"
           ),
       ]
