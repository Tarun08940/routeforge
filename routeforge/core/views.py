from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math


def haversine_km(lat1, lng1, lat2, lng2):
    """
    Calculate great-circle distance between two points on Earth (km)
    """
    R = 6371  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


@csrf_exempt
def route_estimate(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)

    pickup = data["pickup"]
    drop = data["drop"]

    distance_km = haversine_km(
        pickup["lat"], pickup["lng"],
        drop["lat"], drop["lng"]
    )

    avg_speed_kmh = 30  # realistic city average
    duration_min = (distance_km / avg_speed_kmh) * 60

    return JsonResponse({
        "distance_km": round(distance_km, 2),
        "estimated_time_min": round(duration_min, 1)
    })

from django.shortcuts import render

def home(request):
    return render(request, "core/index.html")
