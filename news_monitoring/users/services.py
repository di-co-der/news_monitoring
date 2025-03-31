from news_monitoring.users import models as user_models
from urllib.parse import urlparse

def process_company_form(request):
    """Handles validation and processing of the company form."""
    name = request.POST.get('name', '').strip()
    company_url = request.POST.get('company_url', '').strip()

    if not name or not company_url:
        return False, {'error_message': 'All fields are required.', 'name': name, 'company_url': company_url}

    domain = urlparse(company_url).netloc
    if user_models.Company.objects.filter(company_url__icontains=domain).exists():
        return False, {'error_message': 'A company with this domain already exists.', 'name': name, 'company_url': company_url}

    company = user_models.Company.objects.create(name=name, company_url=company_url, added_by=request.user)
    return True, company
