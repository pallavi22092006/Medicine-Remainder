from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('reminders/', views.ReminderListCreateView.as_view(), name='reminder-list'),
    path('reminders/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder-detail'),
    path('history/', views.MedicineLogListView.as_view(), name='history'),
]
