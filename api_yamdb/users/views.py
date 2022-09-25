from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminOrSuperUser, OwnerOnly
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer,
                          UserSerializerMe)


class APISignup(APIView):
    """Самостоятельная регистрация пользовалеля
    и отправка/переотправка кода подтверждения"""
    permission_classes = []

    def post(self, request):
        """Обрабатываем POST запрос с регистрацией"""
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user_on_email = User.objects.filter(
            email=serializer.data['email']
        ).first()
        user_on_username = User.objects.filter(
            username=serializer.data['username']
        ).first()
        if not user_on_email == user_on_username:
            raise ValidationError(
                'email и username принадлежат разным пользователям'
            )
        user_on_username = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email'],
        )
        self.send_email(user_on_username[0], serializer.data['email'])
        return Response(serializer.data)

    def send_email(self, user, to_email):
        """Отправляем email с кодом подтверждения"""
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'uid': default_token_generator.make_token(user),
        })
        mail_subject = 'Activate your account.'
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


class APIToken(APIView):
    """Выпускаем/перевыпускаем jwt-токен"""
    permission_classes = []

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=serializer.data['username'])
        confirmation_code = serializer.data['confirmation_code']
        check_result_token = default_token_generator.check_token(
            user,
            confirmation_code
        )
        if not check_result_token:
            raise ValidationError(
                'No valid confirmation code'
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token)
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Полное управление пользователями для администратора"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOrSuperUser,)
    lookup_field = "username"

    def get_permissions(self):
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated, OwnerOnly,)
    )
    def get(self, request):
        """Выдаем данные по текущему пользователю
        или частично меняем данне анкеты"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializerMe(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
