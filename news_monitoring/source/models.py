from django.db import models

from news_monitoring.users import models as user_models

# Source Model
class Source(models.Model):
   tagged_company = models.ManyToManyField(user_models.Company, related_name='tagged_sources', blank=True)

   company = models.ForeignKey(user_models.Company, on_delete=models.CASCADE, null=True,blank=True)
   added_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='sources_added')
   updated_by = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='sources_updated', null=True, blank=True)

   name = models.CharField(max_length=255)
   url = models.URLField(unique=True, null=False, blank=False)
   added_on = models.DateTimeField(auto_now_add=True)
   updated_on = models.DateTimeField(auto_now=True)

   # Unique constraint to ensure that company_id and url combination is unique
   class Meta:
       constraints = [
           models.UniqueConstraint(fields=['company', 'url'], name='unique_company_url')
           #check constraint-------------------
       ]
