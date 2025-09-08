from rest_framework import serializers
from .models import Job, JobTask,Equipment
from equipment.serializers import EquipmentSerializer


class JobTaskSerializer(serializers.ModelSerializer):
    required_equipment = EquipmentSerializer(many=True, read_only=True)
    required_equipment_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Equipment.objects.all(),
        write_only=True,
        source='required_equipment'
    )

    job = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = JobTask
        fields = [
            'id', 'job', 'title', 'description', 'status',
            'completed_at', 'order',
            'required_equipment',       # read-only
            'required_equipment_ids'    # write-only 
        ]



class JobSerializer(serializers.ModelSerializer):
    tasks = JobTaskSerializer(many=True, read_only=False)

    class Meta:
        model = Job
        fields = '__all__'

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        job = Job.objects.create(**validated_data)

        for task_data in tasks_data:
            # pop the equipment list before creating
            required_equipment = task_data.pop('required_equipment', [])
            task = JobTask.objects.create(job=job, **task_data)
            if required_equipment:
                task.required_equipment.set(required_equipment)
        return job
    
    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', None)
        instance = super().update(instance, validated_data)

        # Optional: update tasks if provided
        if tasks_data is not None:
            instance.tasks.all().delete()  # simple replace pattern
            for task_data in tasks_data:
                JobTask.objects.create(job=instance, **task_data)
        return instance