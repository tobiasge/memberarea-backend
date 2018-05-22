from django.urls import path

from .views import (
    TagsAPIView, TagAPIView
)

urlpatterns = [
    path('', TagsAPIView.as_view()),
    path('/<int:pk>', TagAPIView.as_view()),
]
