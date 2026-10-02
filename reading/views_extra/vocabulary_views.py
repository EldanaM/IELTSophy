from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import VocabularyWord


@api_view(['GET', 'POST'])
def vocabulary(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)

    if request.method == 'GET':
        words =VocabularyWord.objects.filter(user=request.user).order_by('-added_at')
        return Response([{
            'id': w.id, 'word': w.word,
            'translation': w.translation, 'context': w.context,
        } for w in words])

    if request.method == 'POST':
        word =request.data.get('word', '').strip()
        if not word:
            return Response({'error': 'Word is required'}, status=400)

        w =VocabularyWord.objects.create(
            user =request.user,
            word =word,
            translation =request.data.get('translation', ''),
            context =request.data.get('context', ''),
        )
        return Response({'id': w.id, 'word': w.word}, status=201)


@api_view(['DELETE'])
def delete_word(request, word_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=401)

    try:
        w =VocabularyWord.objects.get(id=word_id, user=request.user)
        w.delete()
        return Response({'success': True})
    except VocabularyWord.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)