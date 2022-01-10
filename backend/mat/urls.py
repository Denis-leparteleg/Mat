from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views


test_patterns = [
	path('', views.index, name='index'),
	path('', views.oauth_success, name='test_oauth_success'),
	path('payment/', views.stk_push_success, name='test_stk_push_success'),
	path('business-payment/success', views.business_payment_success, name='test_business_payment_success'),
	path('salary-payment/success', views.salary_payment_success, name='test_salary_payment_success'),
	path('promotion-payment/success', views.promotion_payment_success, name='test_promotion_payment_success'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('', include(test_patterns)),
    path('accounts/', include('allauth.urls')),
    path('findbus', views.findbus, name="findbus"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
]