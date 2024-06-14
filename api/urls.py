from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', list_users, name='user-list'),
    path('user_get/<int:user_id>/', user_detail_get, name='user-detail_get'),
    path('user_update/<int:user_id>/', user_detail_update, name='user-detail_update'),
    path('user_delete/<int:user_id>/', user_detail_delete, name='user-detail_delete'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('addresses/', list_addresses, name='list-addresses'),
    path('addresses/create/', create_address, name='create-address'),
    path('addresses/<int:address_id>/', get_address, name='get-address'),
    path('addresses/<int:address_id>/update/', update_address, name='update-address'),
    path('addresses/<int:address_id>/delete/', delete_address, name='delete-address'),

]
