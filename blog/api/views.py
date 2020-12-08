from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import generics, mixins, views
from blog.api.serializers import BlogSerializer,LoginSerializer,SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from blog.models import Post

class BlogViewSet(ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=BlogSerializer

class LoginView(APIView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.login(serializer.validated_data))

class SignUpView(APIView):
	serializer_class = SignUpSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save(serializer.validated_data)
		return Response(serializer.data)

class UserProfileApiView(generics.RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		print(self.request.user)
		return self.request.user

