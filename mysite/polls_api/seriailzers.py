from rest_framework import serializers
from polls.models import Question

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data): # 유효성 체크 validated_data
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.save()
        return instance