from datetime import date

from rest_framework import serializers

from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    days_until = serializers.SerializerMethodField()

    class Meta:
        model = Reminder
        fields = ('id', 'person_name', 'occasion', 'date', 'notes', 'days_until', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_days_until(self, obj):
        today = date.today()
        try:
            next_occurrence = obj.date.replace(year=today.year)
        except ValueError:  # Feb 29 on a non-leap year
            next_occurrence = obj.date.replace(year=today.year, day=28)
        if next_occurrence < today:
            next_occurrence = next_occurrence.replace(year=next_occurrence.year + 1)
        return (next_occurrence - today).days
