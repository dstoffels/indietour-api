from rest_framework import serializers
from .models import Band, BandUser
from authentication.serializers import UserSerializer
from authentication.models import User
from rest_framework.exceptions import ValidationError


class BandUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # band_id = serializers.CharField(write_only=True)

    class Meta:
        model = BandUser
        fields = "user", "id", "band_id", "is_admin"

    def create(self, validated_data: dict):
        email = self.initial_data.get("email")
        is_admin = self.initial_data.get("is_admin")

        user, created = User.objects.get_or_create(email=email)

        band: Band = self.context.get("band")

        banduser = BandUser.objects.filter(band=band, user=user)
        if len(banduser):
            raise ValidationError({"details": "Band User already exists", "code": "DUPLICATE"})
        banduser = BandUser.objects.create(band=band, user=user, is_admin=is_admin)

        return banduser


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = "__all__"

    owner = UserSerializer(read_only=True)
    users = BandUserSerializer(source="banduser_set", read_only=True, many=True)
