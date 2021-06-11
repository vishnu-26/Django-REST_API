from rest_framework import generics,mixins
from post.models import BlogPost

from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer
from django.db.models import Q


class BlogPostAPIView(mixins.CreateModelMixin,generics.ListAPIView): 
    lookup_field            = 'pk' 
    serializer_class        = BlogPostSerializer
    permission_classes      = [IsOwnerOrReadOnly]
   

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title=query)|Q(content=query)).distinct()
        return qs


    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def get_serializer_context(self):
        return {'request':self.request}


#class BlogPostListView(generics.ListAPIView):
#    serializer_class = BlogPostSerializer
#    
#    def get_queryset(self):
#        return BlogPost.objects.all()
#


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = BlogPostSerializer
    permission_classes      = [IsOwnerOrReadOnly]
   

    def get_queryset(self):
        return BlogPost.objects.all()

    def get_serializer_context(self,*args,**kwargs):
        return {"request":self.request}



