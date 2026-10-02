from rest_framework import serializers
from .models import Text, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Question
        fields =['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']


class TextSerializer(serializers.ModelSerializer):
    questions =QuestionSerializer(many=True, read_only=True)

    class Meta:
        model =Text
        fields =['id', 'title', 'content', 'level', 'topic', 'questions']