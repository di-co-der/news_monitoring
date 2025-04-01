from django.shortcuts import get_object_or_404

from news_monitoring.source import models as source_models
from news_monitoring.users import models as user_models
from news_monitoring.utils import utils

def process_source_form(request, source_id=None):
    """Handles the logic for processing the source form."""
    is_edit = bool(source_id)

    if is_edit:
        if request.user.is_staff:
            source = get_object_or_404(source_models.Source, id=source_id)
        else:
            source = get_object_or_404(source_models.Source, id=source_id, added_by=request.user)
    else:
        source = None

    error = None
    selected_companies = []

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        url = request.POST.get("url", "").strip()
        tagged_company_ids = request.POST.getlist("tagged_company")

        # Perform validation
        error = validate_source_form(name, url, source_id)

        if not error:
            # Save the source
            if not source:
                source = source_models.Source(added_by=request.user, company=request.user.company)
            source.name = name
            source.url = url
            source.updated_by = request.user
            source.save()

            # Save Many-to-Many field (tagged_company)
            selected_companies = user_models.Company.objects.filter(id__in=tagged_company_ids)
            source.tagged_company.set(selected_companies)

            # If adding a new source, import stories from feed
            if not is_edit:
                utils.import_stories_from_feed(source, request.user)

            return source, is_edit, user_models.Company.objects.all(), list(
                selected_companies.values_list("id", flat=True)), None

    # Fetch existing tagged companies for editing
    if source:
        selected_companies = list(source.tagged_company.values_list("id", flat=True))

    return source, is_edit, user_models.Company.objects.all(), selected_companies, error or ""

def validate_source_form(name, url, source_id):
    """Validates the source form data and returns an error message if any issues are found."""
    if not name or not url:
        return "Name and URL are required."

    if source_models.Source.objects.exclude(id=source_id).filter(url=url).exists():
        return "A source with this URL already exists."

    return None  # No errors
