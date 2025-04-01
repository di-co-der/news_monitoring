from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from news_monitoring.source import services
from news_monitoring.source import models as source_models

@login_required
def source_form(request, source_id=None):
    """Render the source form page, handling both adding and editing a source."""
    source, is_edit, companies, selected_companies, error = services.process_source_form(request, source_id)

    if error:
        messages.error(request, error)
    elif request.method == "POST":
        messages.success(request, f"Source {'updated' if is_edit else 'added'} successfully!")
        return redirect("source:source_list")

    return render(request, "source/add_source.html", {
        "source": source,
        "companies": companies,
        "selected_companies": selected_companies,
        "is_edit": is_edit,
    })

@login_required
def source_list(request):
    # If the logged-in user is staff, show all sources
    if request.user.is_staff:
        sources = source_models.Source.objects.all()
    else:
        # Otherwise, show only the sources added by the logged-in user
        sources = source_models.Source.objects.filter(added_by=request.user)

    # Redirect if user has no sources and is not a staff member
    if not request.user.is_staff and sources.count() == 0:
        return redirect('source:add_source')  # Redirect to the Add Source page

    return render(request, 'source/source_list.html', {'sources': sources})

@login_required
def delete_source(request, source_id):
    source = get_object_or_404(source_models.Source, id=source_id)
    source.delete()
    return redirect('source:source_list')
