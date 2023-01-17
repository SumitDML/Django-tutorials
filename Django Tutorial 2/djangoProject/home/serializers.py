from rest_framework import serializers
from .models import Todo, TimingTodo
import re
from django.template.defaultfilters import slugify


class TodoSerializers(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        # fields = '__all__'
        fields = ['todo_title', 'slug', 'todo_description', 'uid', 'is_done']
        # exclude = ['created_at']

    @staticmethod
    def get_slug(obj):
        return slugify(obj.todo_title)

    @staticmethod
    def validate_todo_title(data):
        if data:
            todo_title = data
            if len(todo_title) < 3:
                raise serializers.ValidationError("less than 3!")

            regex = re.compile('[@_#$%^&*()<>?/\|}{~:]')
            if regex.search(todo_title) is not None:
                raise serializers.ValidationError('to_do title cannot contain a special character!')

        return data


#
class TimingTodoSerializer(serializers.ModelSerializer):
    todo = TodoSerializers()
    class Meta:
        model = TimingTodo
        exclude = ['created_at', 'updated_at']
        # depth =   1  For All fields
