from django.shortcuts import get_object_or_404
from news_monitoring.story.models import Story

def process_story_form(request, story_id=None):
    """Handles validation and processing of the story form."""
    is_edit = bool(story_id)

    if is_edit:
        if request.user.is_staff:
            story = get_object_or_404(Story, id=story_id)
        else:
            story = get_object_or_404(Story, id=story_id, added_by=request.user)
    else:
        story = None

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            return None, is_edit, "Title and Content are required."

        if not is_edit:
            story = Story(added_by=request.user, title=title, content=content)
        else:
            story.title = title
            story.content = content
            story.updated_by = request.user

        story.save()
        return story, is_edit, None  # No error

    return story, is_edit, None  # No error

def get_stories_for_user(user):
    """Fetch stories for the logged-in user based on their company."""
    if user.is_staff:
        return Story.objects.prefetch_related('tagged_company', 'source__tagged_company').all()
    else:
        return Story.objects.prefetch_related('tagged_company', 'source__tagged_company').filter(
            company=user.company
        )
