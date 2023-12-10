from django.urls import path, include

from .views import home, register, user_login, dashboard, logout_view, create_post, edit_post, delete_post, read_more, search_results


urlpatterns = [
    path('search/', search_results, name='search_results'),
    path('read_more/<int:post_id>/', read_more, name='read_more'),
    path('create-post/', create_post, name='create_post'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]
