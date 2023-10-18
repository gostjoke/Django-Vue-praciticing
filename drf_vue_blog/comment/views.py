from django.shortcuts import render
from rest_framework import viewsets
from comment.models import Comment
from comment.serializers import CommentSerializer
from comment.permissions import IsOwnerOrReadOnly

# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class= CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# without permission
# http POST http://127.0.0.1:8000/api/comment/ article=6 content="New comment by Obama"
# with
# http -a will:123  POST http://127.0.0.1:8000/api/comment/ article=1 content="New comment by Obama"