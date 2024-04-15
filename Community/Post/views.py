# myapp/views.py
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector


class PostView(generics.GenericAPIView):  

    def get(self, request):  
        result = Post.objects.all() 
        serializer_class = PostSerializer(result,many=True)  
        return Response({'success': 'success', "students":serializer_class.data}, status=200) 
        
  
    def post(self, request):  
        serializer_class = PostSerializer(data=request.data) 
        if serializer_class.is_valid():  
            serializer_class.save()
            return Response({"status": "success", "data": serializer_class.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)  
  
    def patch(self, request, id):  
        result = Post.objects.get(id=id)  
        serializer_class = PostSerializer(result, data = request.data, partial=True)  
        if serializer_class.is_valid():  
            serializer_class.save()  
            return Response({"status": "success", "data": serializer_class.data})  
        else:  
            return Response({"status": "error", "data": serializer_class.errors})  
  
    def delete(self, request, id=None):  
        result = get_object_or_404(Post, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            search_vector = SearchVector('title', 'content')
            queryset = queryset.annotate(
                search=search_vector
            ).filter(search=search_query)
        return queryset