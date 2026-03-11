from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from sales.views import inicio, ventas, inventario, ingreso_productos, recuperar_cuenta, recuperar_confirmar, registro, editar_producto

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', inicio, name='inicio'),
    path('ventas/', ventas, name='ventas'),
    path('inventario/', inventario, name='inventario'),
    path('ingreso-productos/', ingreso_productos, name='ingreso_productos'),
    path('editar-producto/<int:producto_id>/', editar_producto, name='editar_producto'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('registro/', registro, name='registro'),
    
    path('recuperar-cuenta/', recuperar_cuenta, name='recuperar_cuenta'),
    path('recuperar/<uidb64>/<token>/', recuperar_confirmar, name='recuperar_confirmar'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]