from django.urls import path
from .views import UserSignupView,UserLoginView, UserStatusUpdateAPIView,UserUpdateAPIView,UserListView

urlpatterns = [
    path('sign-up/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
     path('update/', UserUpdateAPIView.as_view(), name='user-update'),
     path('details/',UserListView.as_view(),name='user-list'),
     path('update-status/<int:user_id>/', UserStatusUpdateAPIView.as_view(), name='update_user_status'),

]
