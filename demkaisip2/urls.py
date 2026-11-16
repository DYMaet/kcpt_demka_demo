"""
URL configuration for demkaisip2 project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from demka import views

# Юрлки относятся к views которые вы ранее создавали.

urlpatterns = [
    # Не обязательно, это встроенная админка джанги
    path('admin/', admin.site.urls),
    # name задаёт имя по которому к ссылке можно обращаться в html шаблонах. Удобно для всяких кнопок-ссылок и редиректов
    # Auth pages
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User pages
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-application/', views.create_application_view, name='create_application'),
    #  ниже в <> это аргумент. В нашем случае нужно в качестве аргумента передавать id записи на курс, на который хотим оставить отзыв
    # В шаблоне передаётся подобным образом:
    # {% url 'create_review' app.id %} app.id берём из контекста который передали в view
    path('create-review/<int:application_id>/', views.create_review_view, name='create_review'),

    # Admin panel
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]

# vvv это так по приколу тут, на сервере по-сути должно быть настроено чтобы картинки раздавались без этой темы vvv
# Serve media files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]