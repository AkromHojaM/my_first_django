from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import HomeView, AboutView, GaleryView, ContactView, MenuView, BlogView, ReservationView, ShoppingCardView, \
    IncrementCountAPIView, DecrementCountAPIView, ChangeCountAPIView, AddProductView
from accounts.views import LoginView,RegisterView,LogoutView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/',AboutView.as_view(),name='about'),
    path('menu/',MenuView.as_view(),name='menu'),
    path('blog/',BlogView.as_view(),name="blog"),
    path('galery/',GaleryView.as_view(),name="galery"),
    path('reservation/',ReservationView.as_view(),name="reservation"),
    path('contact/',ContactView.as_view(),name="contact"),
    path('logins/',LoginView.as_view(),name="logins"),
    path('registered/',RegisterView.as_view(),name="registered"),
    path('logouts/',LogoutView.as_view(),name="logouts"),
    path('cart/',ShoppingCardView.as_view(),name="cart"),
    path('add-product/',AddProductView.as_view(),name="add-product"),
    path('reset-password',PasswordResetView.as_view(template_name='password_reset.html'),
         name="reset_password"),
    path('reset-password-done',PasswordResetDoneView.as_view(template_name='passwrod_reset_done.html'),
         name="password_reset_done"),
    path('reset-passwrod/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset-passwrod-complete',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name="password_reset_complete"),
    path('increment/',csrf_exempt(IncrementCountAPIView.as_view()),name='increment'),
    path('decrement/',csrf_exempt(DecrementCountAPIView.as_view()),name='decrement'),
    path('change/',csrf_exempt(ChangeCountAPIView.as_view()),name='change'),]
