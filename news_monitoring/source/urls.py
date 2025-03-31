from django.urls import path

from news_monitoring.source import views

app_name = "source"

urlpatterns = [
    path('source/', views.source_form, name='add_source'),
    path('source/edit/<int:source_id>/', views.source_form, name='edit_source'),
    path('sources/', views.source_list, name='source_list'),
    path('sources/delete/<int:source_id>/', views.delete_source, name='delete_source'),

]
