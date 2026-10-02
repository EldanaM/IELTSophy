from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Text, Question, UserProfile, Achievement, TestSession, Mistake
from ..serializers import TextSerializer
from django.utils import timezone
import random


@api_view(['GET'])
def get_text(request):
    level =request.GET.get('level', 'B1')
    topic =request.GET.get('topic', None)

    texts =Text.objects.filter(level=level)
    if topic and topic.strip() != '':
        texts =texts.filter(topic__iexact=topic)

    if not texts.exists():
        texts =Text.objects.all()

    if not texts.exists():
        return Response({'error': 'No texts found'}, status=404)

    text =random.choice(list(texts))
    return Response(TextSerializer(text).data)


@api_view(['POST'])
def check_answers(request):
    text_id =request.data.get('text_id')
    answers =request.data.get('answers', {})
    time_spent =request.data.get('time_spent', 0)

    if not text_id:
        return Response({'error': 'text_id is required'}, status=400)

    questions =Question.objects.filter(text_id=text_id)
    if not questions.exists():
        return Response({'error': 'No questions found'}, status=404)

    correct =0
    wrong =0
    mistakes =[]

    for q in questions:
        user_answer =str(answers.get(str(q.id), '')).lower().strip()
        if user_answer ==q.correct_option.lower():
            correct +=1
        else:
            wrong +=1
            mistakes.append({
                'question_id': q.id,
                'question_text': q.question_text,
                'your_answer': user_answer,
                'correct_answer': q.correct_option,
            })

    total =correct + wrong
    percent =round(correct / total * 100) if total > 0 else 0

    if request.user.is_authenticated:
        text =Text.objects.get(id=text_id)

        TestSession.objects.create(
            user =request.user,
            text =text,
            correct =correct,
            wrong =wrong,
            percent =percent,
            time_spent =time_spent,
        )

        profile, _ =UserProfile.objects.get_or_create(user=request.user)
        today =timezone.now().date()

        if profile.last_test_date:
            diff =(today - profile.last_test_date).days
            if diff == 1:
                profile.streak +=1
            elif diff > 1:
                profile.streak =1
        else:
            profile.streak =1

        profile.last_test_date =today
        profile.total_tests +=1
        profile.total_correct +=correct
        profile.total_wrong +=wrong

        levels =['B1', 'B2', 'C1', 'C2']
        if profile.level in levels:
            idx =levels.index(profile.level)
            if correct >= 8 and idx < 3:
                profile.level =levels[idx + 1]
            elif correct <= 3 and idx > 0:
                profile.level =levels[idx - 1]

        profile.save()

        for m in mistakes:
            q =Question.objects.get(id=m['question_id'])
            mistake, _ =Mistake.objects.get_or_create(
                user =request.user,
                question_type =q.question_type,
            )
            mistake.count +=1
            mistake.save()

        unlock_achievements(request.user, profile, percent)

    return Response({
        'correct': correct,
        'wrong': wrong,
        'total': total,
        'percent': percent,
        'mistakes': mistakes,
    })


def unlock_achievements(user, profile, percent):
    if profile.total_tests == 1:
        Achievement.objects.get_or_create(
            user =user, code ='first_test',
            defaults ={'title': 'First Test', 'icon': '🎯'}
        )
    if profile.streak >= 3:
        Achievement.objects.get_or_create(
            user =user, code ='streak_3',
            defaults ={'title': '3-Day Streak', 'icon': '🔥'}
        )
    if percent == 100:
        Achievement.objects.get_or_create(
            user =user, code ='perfect',
            defaults ={'title': 'Perfect Score', 'icon': '💯'}
        )
    if profile.total_tests >= 5:
        Achievement.objects.get_or_create(
            user =user, code ='five_tests',
            defaults ={'title': '5 Tests Done', 'icon': '📚'}
        )