from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from news_monitoring.story import services
from news_monitoring.story import models as story_models
from news_monitoring.users import models as user_models

@login_required
def story_form(request, story_id=None):
    """Render the story form page, handling both adding and editing a story."""
    story, is_edit, error = services.process_story_form(request, story_id)

    # Fetch all companies to be used in the form
    companies = user_models.Company.objects.all()

    if error:
        messages.error(request, error)
    elif request.method == "POST":
        messages.success(request, f"Story {'updated' if is_edit else 'added'} successfully!")
        return redirect("story_list")

    return render(request, "story/add_story.html", {
        "story": story,
        "is_edit": is_edit,
        "companies": companies,  # Pass companies to the template
        "selected_companies": story.tagged_company.values_list('id', flat=True) if is_edit else []
    })

@login_required
def story_list(request):
    """Display stories based on the logged-in user's company."""
    stories = services.get_stories_for_user(request.user)
    return render(request, 'story/story_list.html', {'stories': stories})

@login_required
def delete_story(request, story_id):
    """Delete a story and redirect to the story list."""
    story = get_object_or_404(story_models.Story, id=story_id)
    story.delete()
    messages.success(request, "Story deleted successfully!")
    return redirect('story:story_list')
