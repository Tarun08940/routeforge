from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math
from .models import Courier, Delivery


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

def find_nearest_available_courier(pickup_lat, pickup_lng):
    couriers = Courier.objects.filter(is_available=True)

    nearest = None
    min_distance = float("inf")

    for courier in couriers:
        if courier.current_lat is None or courier.current_lng is None:
            continue

        dist = haversine_km(
            pickup_lat, pickup_lng,
            courier.current_lat, courier.current_lng
        )

        if dist < min_distance:
            min_distance = dist
            nearest = courier

    return nearest, min_distance
@csrf_exempt
def create_delivery(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)

    pickup = data["pickup"]
    drop = data["drop"]

    delivery = Delivery.objects.create(
        pickup_lat=pickup["lat"],
        pickup_lng=pickup["lng"],
        drop_lat=drop["lat"],
        drop_lng=drop["lng"],
    )

    courier, courier_distance = find_nearest_available_courier(
        pickup["lat"], pickup["lng"]
    )

    if courier:
        delivery.assigned_courier = courier
        delivery.status = "assigned"
        delivery.save()

        avg_speed = courier.avg_speed_kmh
        eta_min = (courier_distance / avg_speed) * 60
    else:
        eta_min = None

    return JsonResponse({
        "delivery_id": delivery.id,
        "status": delivery.status,
        "courier": courier.name if courier else None,
        "eta_min": round(eta_min, 1) if eta_min else None
    })

def assign_courier(request):
    import json
    data = json.loads(request.body)
    delivery = Delivery.objects.get(id=data['delivery_id'])

    courier = Courier.objects.filter(is_available=True).first()
    if not courier:
        return JsonResponse({'error': 'No couriers available'}, status=400)

    delivery.assigned_courier = courier
    delivery.status = 'assigned'
    delivery.save()

    courier.is_available = False
    courier.save()

    return JsonResponse({
        'courier': courier.name,
        'delivery_status': delivery.status
    })

