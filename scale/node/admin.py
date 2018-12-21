from __future__ import unicode_literals

from django.contrib import admin
from node.models import Node


class NodeAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'is_paused', 'pause_reason', 'is_active', 'deprecated')

admin.site.register(Node, NodeAdmin)
