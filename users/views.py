from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import MyCustomPermission
from rest_framework.permissions import (IsAuthenticated, IsAuthenticatedOrReadOnly)
from .permissions import IsUserOwner, MyUserPermission


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailsViem(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, MyUserPermission]

    def get(self, request: Request, user_id: int) -> Response:

        users = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, users)

        serializer = UserSerializer(instance=users)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:

        users = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, users)

        serializer = UserSerializer(instance=users, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
