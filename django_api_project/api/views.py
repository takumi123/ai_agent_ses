from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers
from celery import shared_task
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

@shared_task
def sample_task(user_id):
    """サンプルの非同期タスク"""
    print(f"Processing task for user {user_id} at {datetime.now()}")
    return True

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email']

    @action(detail=True, methods=['post'])
    def process_async(self, request, pk=None):
        """非同期処理のサンプルエンドポイント"""
        user = self.get_object()
        task = sample_task.delay(user.id)
        return Response({
            'task_id': task.id,
            'status': 'Processing'
        }, status=status.HTTP_202_ACCEPTED)
