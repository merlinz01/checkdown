from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(default="", blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(
        "Status", on_delete=models.SET_NULL, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def closed(self):
        return self.status.closed if self.status else False

    @property
    def nsubtasks(self):
        return Task.objects.filter(parent=self).count()


class Status(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(default="", blank=True)
    order = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default="#808080")
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "statuses"

    def __str__(self):
        return self.name
