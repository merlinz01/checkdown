from django.urls import path, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("tasks", views.TaskViewSet)
router.register("statuses", views.StatusViewSet)
router.register("users", views.UserViewSet)

app_name = "tasks"
urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.APILoginView.as_view()),
    path("logout/", views.APILogoutView.as_view()),
    path("whoami/", views.WhoAmIView.as_view()),
]
