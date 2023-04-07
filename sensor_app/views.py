import io
from datetime import timedelta
import matplotlib.pyplot as plt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import IlluminanceData
from .serializers import IlluminanceDataSerializer


@api_view(['POST'])
def save_illuminance_data(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

    if token != settings.MY_SECRET_KEY:
        return Response({"detail": "Invalid token"}, status=403)

    serializer = IlluminanceDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Check if the number of objects in the database exceeds 9000
        max_objects = 9000
        current_objects = IlluminanceData.objects.count()
        if current_objects > max_objects:
            # Delete the oldest objects exceeding the limit
            objects_to_delete = current_objects - max_objects
            for obj in IlluminanceData.objects.order_by('timestamp')[:objects_to_delete]:
                obj.delete()

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@login_required
def illuminance_chart(request):
    context = {'room_name' : settings.MY_ROOM_NAME}
    return render(request, 'sensor_app/illuminance_chart.html' , context=context)


@api_view(['GET'])
def room_status(request):
    latest_data = IlluminanceData.objects.latest('timestamp')
    is_present = latest_data.value >= 200
    status = "在室" if is_present else "不在"
    latest_time = timezone.localtime(latest_data.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return Response({
        "status": status,
        "is_present": is_present,
        # ここに他のデータを追加できます
        "latest_time" : latest_time,
    })



def create_graph(request):
    now = timezone.now()
    past_24_hours = now - timedelta(hours=24)
    data = IlluminanceData.objects.filter(
        timestamp__gte=past_24_hours).order_by('timestamp')
    timestamps = [timezone.localtime(d.timestamp) for d in data]
    values = [d.value for d in data]

    fig, ax = plt.subplots(figsize=(19, 5))
    ax.plot(timestamps, values)
    ax.set(xlabel='Time', ylabel='Illuminance',
           title=f'Illuminance in {settings.MY_ROOM_NAME}')
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return FileResponse(buf, content_type='image/png')
