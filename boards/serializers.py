from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Workspace, Board, Tag, Task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name',
        required=False
    )
    assignee = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'due_date',
            'status', 'tags', 'board', 'assignee', 'created'
        ]
        read_only_fields = ['created']


        
class BoardSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(BoardSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.fields['workspace'].queryset = Workspace.objects.filter(owner=request.user)
            
    class Meta:
        model = Board
        fields = ['id', 'workspace', 'title', 'created']

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owner', 'members', 'created']
