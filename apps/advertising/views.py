from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AdCreative, AdImpression


@csrf_exempt
@require_POST
def track_impression(request):
    """Record an ad impression or click via AJAX beacon."""
    creative_id = request.POST.get("creative_id")
    event_type = request.POST.get("event_type", "impression")

    if event_type not in ("impression", "click"):
        return JsonResponse({"status": "error"}, status=400)

    try:
        creative = AdCreative.objects.get(pk=creative_id)
    except (AdCreative.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"status": "error"}, status=404)

    AdImpression.objects.create(
        creative=creative,
        event_type=event_type,
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        ip_address=request.META.get("REMOTE_ADDR"),
        referrer=request.META.get("HTTP_REFERER", "")[:200],
    )
    return JsonResponse({"status": "ok"})
