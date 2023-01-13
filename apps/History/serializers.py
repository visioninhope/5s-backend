import datetime

from .models import History

from rest_framework import serializers

from ..Locations.models import Location
from ..Employees.models import CustomUser

class HistorySerializer(serializers.ModelSerializer):
    """
    Create a History record if employee is authenticated, else
    write record with this unknown user and make history record
    """

    def create(self, validated_data):
        if validated_data['action'] == 'entrance' and validated_data['name_file'] != 'unknown':
            print(f'[INFO] validation data is: %s' % validated_data)
        
            image = validated_data['image']
            camera = validated_data['camera']
            action = validated_data['action']
            name_file = validated_data['name_file']
            id_people = int(((f"{validated_data['name_file']}").split('_')[-1]).split('.')[0])
            location = Location.objects.filter(gate_id__camera_input__id=validated_data['camera'])[0]
            history_data = History(
                camera=camera,
                action=action,
                name_file=name_file,
                location=location,
                people=CustomUser.objects.get(id=id_people),
                image=image
            )
            history_data.save()

            user = CustomUser.objects.filter(id=id_people)
            user.update(status=True, location=location)
            return history_data

        elif validated_data['action'] == 'exit' and validated_data['name_file'] != 'unknown':
            image = validated_data['image']
            camera = validated_data['camera']
            action = validated_data['action']
            name_file = validated_data['name_file']
            id_people = int(((f"{validated_data['name_file']}").split('_')[-1]).split('.')[0])
            location = Location.objects.filter(gate_id__camera_output__id=validated_data['camera'])[0]
            release_date = datetime.datetime.now()
            history_data = History(
                camera=camera,
                action=action,
                name_file=name_file,
                location=location,
                release_date=release_date,
                people=CustomUser.objects.get(id=id_people),
                image=image
            )
            history_data.save()

            user = CustomUser.objects.filter(id=id_people)
            user.update(status=False, location=None)
            return history_data

        elif validated_data['name_file'] == 'unknown':
            image = validated_data['image']
            camera = validated_data['camera']
            action = validated_data['action']

            release_date = []
            location = []
            if validated_data['action'] == 'entrance':
                release_date.append(None)
                location.append(Location.objects.get(gate_id__camera_input__id=validated_data['camera']))
            else:
                if validated_data['action'] == 'exit':
                    release_date.append(f"{datetime.datetime.now()}")
                    location.append(Location.objects.get(gate_id__camera_output__id=validated_data['camera']))
            history_data = History(
                camera=camera,
                action=action,
                release_date=release_date[0],
                name_file=None,
                location=location[0],
                people=None,
                image=image
            )
            history_data.save()
            return history_data

        return

    class Meta:
        model = History
        fields = ['id', 'people', 'location', 'image', 'entry_date', 'release_date', 'camera', 'name_file', 'action']
        read_only_fields = ['entry_date']