from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import PreparingVideo


@api_view(['GET'])
def get_videos(request):
    videos =PreparingVideo.objects.all().order_by('-date')[:6]
    data =[{
        'id': v.id,
        'title': v.title,
        'description': v.description,
        'tag': v.tag,
        'type': v.type,
        'url': v.url or '',
    } for v in videos]
    return Response(data)