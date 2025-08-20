from rest_framework import viewsets, permissions
from .models import Workspace, Board, Tag, Task
from .serializers import WorkspaceSerializer, BoardSerializer, TagSerializer, TaskSerializer
from .permissions import IsWorkspaceOwner,IsTaskInOwnedWorkspace
from rest_framework.permissions import IsAuthenticated


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwner]
    
    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        workspace.members.add(self.request.user)
          
    def get_queryset(self):
        return Workspace.objects.filter(members=self.request.user)



class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Board.objects.filter(workspace__members=self.request.user)
    
   
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskInOwnedWorkspace]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            board__workspace__members=user
        ) 
