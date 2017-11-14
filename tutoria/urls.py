"""tutoria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from home import views as home_views
from offering import views as offer_views
from booking import views as book_views
from transaction import views as transaction_views


urlpatterns = [
    url(r'^$', home_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', home_views.signup, name='signup'),
    url(r'^passwordResetRequest/$', home_views.passwordResetRequest, name='passwordResetRequest'),
    url(r'^passwordReset/$', home_views.passwordReset, name='passwordReset'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^offerslot/$', offer_views.offerslot, name='offerslot'),
    url(r'^search/$', book_views.search, name='search'),
    url(r'^booking/(?P<pk>\d+)/$', book_views.booking, name='booking'),
    url(r'^confirmBooking/(?P<pk>\d+)/$', book_views.confirmBooking, name='confirmBooking'),
    url(r'^cancelConfirmBooking/(?P<pk>\d+)/$', book_views.cancelConfirmBooking, name='cancelConfirmBooking'),
    url(r'^confirmCanceling/(?P<pk>\d+)/$', book_views.confirmCanceling, name='confirmCanceling'),
    url(r'^cancelConfirmCanceling/$', book_views.cancelConfirmCanceling, name='cancelConfirmCanceling'),
    url(r'^session/$', book_views.session, name='session'),
    url(r'^sessionHistory/$', book_views.sessionHistory, name='sessionHistory'),
    url(r'^canceling/(?P<pk>\d+)/$', book_views.canceling, name='canceling'),
    url(r'^wallet/$', transaction_views.wallet, name='wallet'),
    url(r'^wallet/history/$', transaction_views.transactionHistory, name='transactionHistory'),
    url(r'^wallet/add/$', transaction_views.addBalanceRequest, name='addBalance'),
    url(r'^wallet/withdraw/$', transaction_views.withdrawBalanceRequest, name='withdrawBalance'),
    url(r'^profile/', book_views.session, name='profile'),
    url(r'^admin/', admin.site.urls),
]
