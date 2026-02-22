from rest_framework import serializers
from .models import Chronology
from apps.event.models import Event
from apps.branch.models import Branch
from rest_framework.response import Response
from collections import defaultdict

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            'id', 'name', 'slug',
            'description', 'is_main',
            'created_by', 'events'
        ]

    def get_events(self, obj):
        events = obj.events.all()\
            .select_related("prev_event")\
            .prefetch_related("actors")\
            .order_by("time_label", "date_label")

        grouped = defaultdict(list)

        for event in events:
            grouped[event.time_label].append(
                EventSerializer(event).data
            )

        return grouped



class ChronologySerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    class Meta:
        model = Chronology
        fields = ["id", "title", "slug", "description", "start_date", "end_date", "created_by", "branch"]
        read_only_fields = ["created_by"]

    def get_created_by(self, obj):
        return obj.created_by.username
    
    def get_branch(self, obj):
        request = self.context.get("request")
        branch = request.query_params.get("branch")
        if branch:
            return BranchSerializer(obj.branches.filter(slug=branch).first()).data
        return BranchSerializer(obj.branches.filter(is_main=True).first()).data