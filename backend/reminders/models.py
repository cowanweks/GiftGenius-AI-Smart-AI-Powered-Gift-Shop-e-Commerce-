from django.conf import settings
from django.db import models


class Reminder(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    person_name = models.CharField(max_length=150)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, default='birthday')
    date = models.DateField(help_text='The month and day repeat every year')
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.person_name} - {self.occasion} ({self.date})'
