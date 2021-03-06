from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views


test_patterns = [
    path('', views.home, name="home"),
	path('', views.oauth_success, name='test_oauth_success'),
	path('payment/', views.stk_push_success, name='test_stk_push_success'),
	path('business-payment/success', views.business_payment_success, name='test_business_payment_success'),
	path('salary-payment/success', views.salary_payment_success, name='test_salary_payment_success'),
	path('promotion-payment/success', views.promotion_payment_success, name='test_promotion_payment_success'),
]

urlpatterns = [
    path('', views.home, name="home"),
    path('findmat', views.findmat, name="findmat"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('about/', views.about, name='about'),
    path('payment/', views.payment, name='payment'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('', include(test_patterns)),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('account/', include('allauth.urls')),
    path('account/', include('django.contrib.auth.urls')),
]