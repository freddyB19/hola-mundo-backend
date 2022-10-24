from django.contrib.auth import authenticate
from rest_framework import serializers, pagination
from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ("id", "nombre", "apellido", "edad")
        read_only_fields = ("id", )
        extra_kwargs = {
            "nombre":{"min_length":4, "max_length":50},
            "apellido":{"min_length":4, "max_length":50},
            "edad":{"style":{"input_type":"number"}},
        }

    def validate_edad(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Ingrse una edad Correcta")
        return value

    def save(self):
        person = models.Person(
            nombre = self.validated_data.get("nombre"),
            apellido = self.validated_data.get("apellido"),
            edad = self.validated_data.get("edad")
        )
        person.save()
        return person

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sesion
        fields = "__all__"


class ModuloDetalleSerializer(serializers.ModelSerializer):
    # modulo_sesion = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='sesion-detail',
    # )
    levels = serializers.SerializerMethodField()
    class Meta:
        model = models.Modulo
        fields = ("__all__")

    def get_levels(self, obj):
        all_levels = obj.modulo_sesion.all()
        data = []
        for level in all_levels:
            sesion = models.Sesion.objects.get(url = level)
            data.append({
                "title": sesion.title,
                "level": sesion.get_absolute_url(),
                "checkpoint": sesion.checkpoint
            })
        return data

# class ModuloSerializer(serializers.ModelSerializer):
#     #modulo_sesion = SesionSerializer(read_only = True, many = True)
#     count = serializers.IntegerField()
#     class Meta:
#         model = models.Modulo
#         fields = ("id", "num_modulo", "title", "url" "count")

class ModuloSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    num_modulo = serializers.IntegerField()
    title = serializers.CharField()
    count = serializers.IntegerField()
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        return obj.get_absolute_url()




class ProgresoPersonSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only = True)
    class Meta:
        model = models.ProgresoPerson
        fields = ("url", "next", "puntos", "created", "person")
