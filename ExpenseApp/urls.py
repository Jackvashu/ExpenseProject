from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('Home/',views.home, name="home"),
    path('Add-Transaction/',views.addTransaction, name='add_transaction'),
    path('profile/',views.addProfile, name="profile"),
    path('show-transaction/', views.showTransactionList, name="showTransactionList")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
