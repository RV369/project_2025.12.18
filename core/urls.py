from django.urls import path

from core import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/delete/', views.delete_account, name='delete_account'),
    path('auth/profile/', views.update_profile, name='update_profile'),
    path('products/', views.products_list, name='products_list'),
    path(
        'products/<int:product_id>/',
        views.product_detail,
        name='product_detail',
    ),
    path('access-rules/', views.access_rules, name='access_rules'),
]
