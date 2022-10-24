from rest_framework import serializers
from applications.game import models

from applications.users.apiv1.serializers import UserProfileSerializer

class SesionSerializer(serializers.ModelSerializer):
    modulo_detail = serializers.SerializerMethodField()

    class Meta:
        model = models.Sesion
        fields = "__all__"

    def get_modulo_detail(self, obj):
        data = {
            "id": obj.modulo.id,
            "title": obj.modulo.title,
            "url": obj.modulo.url
        }
        return data


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
        all_levels = obj.modulo_sesion.all().order_by("num_sesion")
        data = []
        for level in all_levels:
            sesion = models.Sesion.objects.get(url = level)
            data.append({
                "title": sesion.title,
                "level": sesion.get_absolute_url(),
                "checkpoint": sesion.checkpoint,
                "url": sesion.url,
                "id": sesion.id
            })
        return data

class ModuloSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    active = serializers.BooleanField()
    checkpoint = serializers.IntegerField()
    num_modulo = serializers.IntegerField()
    url = serializers.SlugField()
    image = serializers.ImageField()
    title = serializers.CharField()
    introduccion = serializers.CharField()
    count = serializers.IntegerField()
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        return obj.get_absolute_url()




class ProgresoPlayerSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(read_only = True)
    path = serializers.SerializerMethodField()
    class Meta:
        model = models.ProgresoPlayer
        fields = ("url", "next", "puntos", "created", "path")

    def get_path(self, obj):
        return models.Sesion.objects.get(checkpoint = obj.puntos).title
