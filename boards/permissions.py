from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWorkspaceOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.owner == request.user or request.user in obj.members.all()
        
        return obj.owner == request.user


class IsTaskInOwnedWorkspace(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return (
                obj.board.workspace.owner == request.user or 
                request.user in obj.board.workspace.members.all()
            )

        return obj.board.workspace.owner == request.user
