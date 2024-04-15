# myapp/views.py
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector



class CommentView(generics.GenericAPIView):  

    def get(self, request):  
        result = Comment.objects.all() 
        serializer_class = CommentSerializer(result,many=True)  
        return Response({'success': 'success', "students":serializer_class.data}, status=200) 
        
  
    def post(self, request):  
        serializer_class = CommentSerializer(data=request.data) 
        if serializer_class.is_valid():  
            serializer_class.save()
            return Response({"status": "success", "data": serializer_class.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)  
  
    def patch(self, request, id):  
        result = Comment.objects.get(id=id)  
        serializer_class = CommentSerializer(result, data = request.data, partial=True)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data})  
        else:  
            return Response({"status": "error", "data": serializer_class.errors})  
  
    def delete(self, request, id=None):  
        result = get_object_or_404(Comment, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})
    
    def upvote(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.upvote += 1
        comment.save()
        return Response({"status": "success", "data": "Upvoted"})

    def downvote(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.downvote += 1
        comment.save()
        return Response({"status": "success", "data": "Downvoted"})
    
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            search_vector = SearchVector('comment')
            queryset = queryset.annotate(
                search=search_vector
            ).filter(search=search_query)
        return queryset
