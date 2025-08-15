from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from boards.models import Workspace, Board, Tag, Task
from datetime import date


class WorkspaceAPICreateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hadi', password='jadi1234')
        self.client.login(username='hadi', password='jadi1234')
        self.url = '/APIworkspaces/'

    def test_create_workspace(self):
        data = {'name': 'My Workspace'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workspace.objects.count(), 1)
        ws = Workspace.objects.first()
        self.assertEqual(ws.name, 'My Workspace')
        self.assertEqual(ws.owner, self.user)
        self.assertIn(self.user, ws.members.all())


class BoardAPICreateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hadi', password='jadi1234')
        self.client.login(username='hadi', password='jadi1234')
        self.workspace = Workspace.objects.create(name='workspace 5', owner=self.user)
        self.workspace.members.add(self.user)
        self.url = f'/boards/'

    def test_create_board(self):
        data = {'title': 'My Board', 'workspace': self.workspace.pk}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        board = Board.objects.first()
        self.assertEqual(board.title, 'My Board')
        self.assertEqual(board.workspace, self.workspace)

class TagAPICreateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hadi', password='jadi1234')
        self.client.login(username='hadi', password='jadi1234')
        self.url = '/tags/'

    def test_create_tag(self):
        data = {'name': 'New tag'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.first()
        self.assertEqual(tag.name, 'New Feature')


class TaskAPICreateTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hadi', password='jadi1234')
        self.client.login(username='hadi', password='jadi1234')
        self.workspace = Workspace.objects.create(name='workspace 5', owner=self.user)
        self.workspace.members.add(self.user)
        self.board = Board.objects.create(title='board Cppp', workspace=self.workspace)
        self.tag = Tag.objects.create(name='Bug Fixl')
        self.url = '/tasks/'

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description':'This is a test task',
            'board': self.board.pk,
            'start_date': date(2025, 8, 10),
            'end_date': date(2025, 8, 15),
            'due_date': date(2025, 8, 20),
            'status': 'todo',
            'assignee': self.user.username,
            'tags' : [self.tag.name],
        }
        response = self.client.post(self.url, data)
        print(response.status_code)
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.board, self.board)
