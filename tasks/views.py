from .models import Task, Status, User
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.authentication import BasicAuthentication
from django.db.models import Q

from rest_framework import (
    permissions,
    viewsets,
    response,
    views as rest_views,
)
from django_filters import rest_framework as filters, BooleanFilter, FilterSet

from .serializers import TaskSerializer, StatusSerializer, UserSerializer


class TaskFilter(FilterSet):
    toplevel = BooleanFilter(field_name="parent", lookup_expr="isnull")

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "assignee",
            "due_date",
            "priority",
            "parent",
            "toplevel",
        ]


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """

    queryset = Task.objects.all().order_by("-due_date", "name")
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TaskFilter


class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows statuses to be viewed or edited.
    """

    queryset = Status.objects.all().order_by("order", "name")
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["name", "closed"]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.filter(is_staff=False).order_by("username")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["username", "email", "first_name", "last_name"]


class APILoginView(rest_views.APIView):
    """
    API endpoint that allows users to log in.
    """

    authentication_classes = [BasicAuthentication]

    def get_authenticate_header(self, request):
        return None

    @method_decorator(never_cache)
    def post(self, request, *args, **kw):
        """Security check complete. Log the user in."""
        request.sensitive_post_parameters = "__ALL__"
        auth_login(self.request, request.user)
        user = UserSerializer(request.user).data
        return response.Response({"success": True, "user": user})


class APILogoutView(rest_views.APIView):
    """
    API endpoint that allows users to log out.
    """

    def get_authenticate_header(self, request):
        return None

    @method_decorator(never_cache)
    def post(self, request, *args, **kw):
        auth_logout(self.request)
        return response.Response({"success": True})


class WhoAmIView(rest_views.APIView):
    """
    API endpoint that allows users to retrieve their user info.
    """

    def get(self, request, *args, **kw):
        if request.user and request.user.is_authenticated:
            return response.Response(UserSerializer(request.user).data)
        return response.Response({"detail": "Not logged in"}, status=401)
