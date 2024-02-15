from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importation de vos ViewSets
from comments.views import CommentViewSet
from contributors.views import ContributorViewSet
from issues.views import IssueViewSet
from projects.views import ProjectViewSet
from users.views import UserViewSet, AuthViewSet, CustomUserViewSet

# Création d'une instance de DefaultRouter
router = DefaultRouter()

# Enregistrement de vos ViewSets avec le routeur
router.register(r'users', UserViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'user-actions', CustomUserViewSet, basename='user-actions')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'contributors', ContributorViewSet, basename='contributors')
router.register(r'issues', IssueViewSet, basename='issues')
router.register(r'comments', CommentViewSet, basename='comments')

# Configuration des URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Inclusion des routes gérées par le routeur DRF
]
