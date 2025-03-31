from django.urls import path

from news_monitoring.story import views

app_name = "story"  # Required for namespacing

urlpatterns = [
    path('story/', views.story_form, name='add_story'),
    path('story/edit/<int:story_id>/', views.story_form, name='edit_story'),
    path('stories/', views.story_list, name='story_list'),
    path('stories/delete/<int:story_id>/', views.delete_story, name='delete_story'),

]
