from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import UserProfile, Achievement, Mistake, TestSession


@api_view(['GET'])
def get_profile(request):
    user =request.user
    if not user.is_authenticated:
        return Response({
            'username': 'Guest', 'level': 'B1', 'streak': 0,
            'total_tests': 0, 'avg_percent': 0, 'forecast_band': '-',
            'achievements': [], 'weak_areas': [],
        })

    profile, _ =UserProfile.objects.get_or_create(user=user)
    achievements =Achievement.objects.filter(user=user)
    mistakes =Mistake.objects.filter(user=user).order_by('-count')[:5]

    return Response({
        'username': user.username,
        'level': profile.level,
        'streak': profile.streak,
        'total_tests': profile.total_tests,
        'avg_percent': profile.avg_percent,
        'forecast_band': profile.forecast_band,
        'achievements': [{'title': a.title, 'icon': a.icon} for a in achievements],
        'weak_areas': [{'type': m.question_type, 'count': m.count} for m in mistakes],
    })


@api_view(['GET'])
def get_history(request):
    if not request.user.is_authenticated:
        return Response([])

    sessions =TestSession.objects.filter(user=request.user).order_by('-started_at')[:20]
    return Response([{
        'id': s.id,
        'text_title': s.text.title,
        'text_level': s.text.level,
        'percent': s.percent,
        'correct': s.correct,
        'wrong': s.wrong,
        'time_spent': s.time_spent,
        'date': s.started_at.strftime('%d %B %Y, %H:%M'),
    } for s in sessions])