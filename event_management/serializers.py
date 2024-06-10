from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from event_management.models import Event

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer
    """
    start_date = serializers.DateField(input_formats=['%d-%m-%Y'])
    end_date = serializers.DateField(input_formats=['%d-%m-%Y'])
    attendees = serializers.ListSerializer(child=serializers.CharField(), required=False)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'attendees', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        """
        function to add new event records
        :param validated_data: validated data of event (dict)
        :return: event model object (obj)
        """
        attendees = validated_data.pop('attendees', [])
        instance = super().create(validated_data)
        self.add_attendees(instance, attendees)
        return instance

    def update(self, instance, validated_data):
        """
        function to update already existed event record
        :param instance: event model object (obj)
        :param validated_data: validated data of event (dict)
        :return: event model object (obj)
        """
        attendees = validated_data.pop('attendees', [])
        super().update(instance, validated_data)
        self.add_attendees(instance, attendees)
        return instance

    @staticmethod
    def add_attendees(obj, attendees):
        """
        function to add attendees related with the event
        :param obj: event model object (obj)
        :param attendees: list of attendees (list)
        :return: None
        """
        for id in attendees:
            try:
                user = User.objects.get(pk=id)
                obj.attendees.add(user)
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'error': f'Attendee {id} does not exist'})

    def get_attendees(self, obj):
        """
        function to get attendees relevant to the event
        :param obj: event model object (obj)
        :return: list of attendees emails (list)
        """
        return [attendee.email for attendee in obj.attendees.all()]
