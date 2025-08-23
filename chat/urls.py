from django.urls import path
from .views import main,get_messages
from .constants import MESSAGES_VIEW_PATH

urlpatterns = [
    path('',main),
    path(MESSAGES_VIEW_PATH,get_messages().as_view()),
]