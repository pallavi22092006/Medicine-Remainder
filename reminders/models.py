from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user: collects name, email, phone. Logs in with email."""
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Reminder(models.Model):
    FREQUENCY_CHOICES = [
        ('Once', 'Once'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('As Needed', 'As Needed'),
    ]
    ALARM_CHOICES = [
        ('chime', 'Gentle Chime'),
        ('beep', 'Classic Beep'),
        ('urgent', 'Urgent Alarm'),
        ('bell', 'Bell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    time = models.TimeField()  # stored as HH:MM:SS, exposed to the API as HH:MM
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='Daily')
    alarm_sound = models.CharField(max_length=20, choices=ALARM_CHOICES, default='chime')
    last_taken_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return f'{self.medicine_name} ({self.time}) — {self.user.email}'


class MedicineLog(models.Model):
    """One row per time a reminder was marked as taken — the history trail."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    reminder = models.ForeignKey(Reminder, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-taken_at']

    def __str__(self):
        return f'{self.medicine_name} taken at {self.taken_at} — {self.user.email}'
