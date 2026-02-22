from django.shortcuts import render
from collections import defaultdict
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .models import Chronology
from .serializers import ChronologySerializer
from apps.event.models import Event
from django.http import HttpResponseNotFound
from django.db.models import Count


class ChronologyDetailView(generics.RetrieveAPIView):
    queryset = Chronology.objects.all()
    serializer_class = ChronologySerializer
    lookup_field = "slug"


def chronology_line(request, slug):
    branch_id = request.GET.get("branch_id", "")
    chronology = Chronology.objects.prefetch_related(
        'branches__events',
        'branches' 
    ).get(slug=slug)

    if branch_id:
        branch = chronology.branches.filter(uuid=branch_id).first()
    else:
        branch = chronology.branches.filter(is_main=True).first()
    if not branch:
        return HttpResponseNotFound("Branch not found")
    events = branch.events.order_by("time_label", "date_label")

    grouped = defaultdict(list)

    for event in events:
        grouped[event.time_label].append(event)


    return render(request, "chronology/vertical_line.html", {
        "chronology": chronology,
        "branch": branch,
        "grouped_events": dict(grouped)
    })


def event_detail(request, slug):
    event = Event.objects.select_related("branch").prefetch_related("branch__events").get(slug=slug)
    return render(request, "chronology/event_details.html", {"event": event})



def homepage(request):
    chronologies = Chronology.objects.prefetch_related(
        'branches', 'branches__events'
    ).select_related('created_by').order_by('-created_at')

    from django.db.models import Sum
    agg = Chronology.objects.aggregate(
        total_branches=Count('branches', distinct=True),
        total_events=Count('branches__events', distinct=True),
    )

    return render(request, 'chronology/homepage.html', {
        'chronologies': chronologies,
        'total_chronologies': chronologies.count(),
        'total_branches': agg['total_branches'] or 0,
        'total_events': agg['total_events'] or 0,
    })
