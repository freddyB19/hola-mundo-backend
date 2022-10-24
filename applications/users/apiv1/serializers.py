from rest_framework import serializers

from applications.users import models

class UserProfileRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only = True)
    class Meta:
        model = models.UserProfile
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def save(self):
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")

        if password != password2:
            raise serializers.ValidationError({"error":"La contraseña de confirmación no es la correcta"})

        if models.UserProfile.objects.filter(email = self.validated_data.get("email")).exists():
            raise serializers.ValidationError({"error":"Ya existe un registro con ese email"})

        if models.UserProfile.objects.filter(username = self.validated_data.get("username")).exists():
            raise serializers.ValidationError({"error":"Ya existe un registro con ese username"})

        user = models.UserProfile.objects.create_user(
            email = self.validated_data.get("email"),
            username = self.validated_data.get("username"),
            password = self.validated_data.get("password"),
            name = self.validated_data.get("name"),
            last_name = self.validated_data.get("last_name"),
            image = self.validated_data.get("image", None),
        )
        return user.save()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = (
            "id",
            "username",
            "email",
            "name",
            "last_name"
        )


class UserProfileSerializer2(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    username = serializers.CharField()
    name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField()


class UserProfileDateTimeData(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ("date_joined", "last_login")
