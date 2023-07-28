from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from .serializers import (
    RegisterSer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSer,
    ChangePasswordSer,
    ProfileSer,
    ActiveResendSer,
    ResetPasswordSer,
)

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile, User
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.conf import settings

# from django.core.mail import send_mail

from mail_templated import send_mail, EmailMessage  # email
from ..utils import EmailThread

# from django.contrib.auth import get_user_model #another way to get User
# User = get_user_model()


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSer

    def post(self, request, *args, **kwargs):
        ser = RegisterSer(data=request.data)
        if ser.is_valid():
            ser.save()
            data = {"email": ser.validated_data["email"]}
            user_obj = get_object_or_404(User, email=ser.validated_data["email"])
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation.tpl",
                {"token": token},
                "admin@admin.com",
                to=[ser.validated_data["email"]],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


# overside this class for change serializer class of this
# class CustomAuthToken(ObtainAuthToken):
#     serializer_class = CustomAuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         token, created = Token.objects.get_or_create(user=user)
#         return Response(
#             {"token": token.key, "user_id": user.pk, "email": user.email}
#         )


# class CustomDiscardAuthToken(APIView): # we write it completely. ObtainAuthToken doesnt have logout
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         request.user.auth_token.delete() #delete token
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(
    TokenObtainPairView
):  # overwrite this class for use custom serializer
    serializer_class = CustomTokenObtainPairSer


class ChangePasswordView(GenericAPIView):
    model = User
    serializer_class = ChangePasswordSer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        ser = self.serializer_class(data=request.data)

        if ser.is_valid():
            if not self.object.check_password(ser.data.get("old_password")):
                return Response(
                    {"detail": "password is not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(ser.data.get("new_password"))
            self.object.save()
            return Response({"detail": "change password successfully"})
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class SendEmailTest(GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = "admin@admin.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/hello.tpl",
            {"token": token},
            "admin@admin.com",
            to=["mamad@gamil.com"],
        )
        EmailThread(email_obj).start()
        return Response("email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = token.get("user_id")
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        user.save()

        return Response({"detail": "user verified successfully"})


class ActivationResend(GenericAPIView):
    serializer_class = ActiveResendSer

    def post(self, request, *args, **kwargs):
        ser = ActiveResendSer(data=request.data)
        ser.is_valid(raise_exception=True)  # instead of if ser.is_valid():
        user_obj = ser.validated_data["user"]  # get user from serializer
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "verification resend successfully"}, status=status.HTTP_200_OK
        )

    # return Response({'detail':'your information invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ResetPassword(GenericAPIView):
    # serializer_class = ResetPasswordSer
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ser = ResetPasswordSer(data=request.data)
        # ser.is_valid(raise_exception=True) #instead of if ser.is_valid():
        # user_obj = ser.validated_data['user'] #get user from serializer
        token = self.get_tokens_for_user(self.object)
        email_obj = EmailMessage(
            "email/reset_pass.tpl",
            {"token": token},
            "admin@admin.com",
            to=[self.object.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "reset password mail sent"}, status=status.HTTP_200_OK
        )

    # return Response({'detail':'your information invalid'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ResetPassword2(GenericAPIView):
    serializer_class = ResetPasswordSer

    def post(self, request, token, *args, **kwargs):
        ser = ResetPasswordSer2(data=request.data)
        ser.is_valid(raise_exception=True)
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = token.get("user_id")
        user_obj = User.objects.get(pk=user_id)
        user_obj.set_password(ser.data.get("new_password"))
        user_obj.save()
        return Response(
            {"detail": "password changed successfully"}, status=status.HTTP_200_OK
        )
