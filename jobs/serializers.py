from rest_framework import serializers
from .models import Job, JobTask
from equipment.serializers import EquipmentSerializer

class JobTaskSerializer(serializers.ModelSerializer):
    required_equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = JobTask
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    tasks = JobTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
