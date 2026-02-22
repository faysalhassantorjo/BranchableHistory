from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Event, Branch


@require_POST
@login_required
def create_event(request):
    title    = request.POST.get('title', '').strip()
    summary  = request.POST.get('summary', '').strip()
    content  = request.POST.get('content', '').strip()
    location = request.POST.get('location', '').strip()
    date_label  = request.POST.get('date_label', '').strip()
    time_label  = request.POST.get('time_label', '').strip()
    branch_uuid = request.POST.get('branch', '').strip()
    prev_slug   = request.POST.get('prev_event', '').strip()

    # Validate required fields
    if not all([title, summary, date_label, branch_uuid]):
        return JsonResponse({'error': 'Missing required fields.'}, status=400)

    branch = get_object_or_404(Branch, uuid=branch_uuid)

    # Resolve prev_event (optional)
    prev_event = None
    if prev_slug:
        prev_event = get_object_or_404(Event, slug=prev_slug)

    event = Event.objects.create(
        title      = title,
        summary    = summary,
        content    = content,
        location   = location,
        date_label = date_label,
        time_label = time_label,
        branch     = branch,
        prev_event = prev_event,
        writer     = request.user,
    )

    # Redirect back to the timeline, scrolling to the new event
    timeline_url = f"/chronology/{branch.chronology.slug}/#event-{event.slug}"
    return redirect(timeline_url)