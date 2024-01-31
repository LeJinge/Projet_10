from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer
from users.utils import send_verification_email


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        # Récupérez le mot de passe et sa confirmation de la requête
        password = self.request.data.get('password')
        password2 = self.request.data.get('password2')

        # Vérifiez que les deux mots de passe correspondent
        if password != password2:
            return Response({"password": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

        # Validez le mot de passe en utilisant validate_password
        try:
            validate_password(password, self.request.user)
        except Exception as e:
            return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'âge minimum
        age = serializer.validated_data.get('age', 0)
        if age < 15:
            # Si l'âge est inférieur à 15 ans, définir les champs sur False
            serializer.validated_data['can_be_contacted'] = False
            serializer.validated_data['can_be_shared'] = False

        # Créer l'utilisateur
        user = serializer.save()
        user.set_password(password)
        user.save()
        send_verification_email(user)  # Envoyer l'email de vérification

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def partial_update_user(self, request, pk=None):
        user = self.get_object()
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user  # Assurez-vous que votre serializer a un moyen d'accéder à l'instance de l'utilisateur
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request):
        # La déconnexion se fait principalement côté client en supprimant le token
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Vérifiez si l'ancien mot de passe est correct
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            # Définir le nouveau mot de passe
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()

            return Response({"message": "Mot de passe modifié avec succès"}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['post'], detail=False)
    def verify_email(self, request):
        token = request.data.get('token')
        try:
            user = self.get_queryset().get(email_confirm_token=token)
            user.email_confirmed = True
            user.save()
            return Response({"message": "Email vérifié avec succès"})
        except CustomUser.DoesNotExist:
            return Response({"message": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)
