from rest_framework import serializers

from post.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=BlogPost
        fields=[
            'url',
            'pk',
            'user',
            'title',
            'content',
            'timestamp'
        ]
#        read_only_fields=['id','user']
        
    def get_url(self,obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


    def validate_title(self,value):
        qs=BlogPost.objects.filter(title=value)         #including instance itself
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The title must be unique")
        return value
