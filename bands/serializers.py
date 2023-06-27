from rest_framework import serializers
from .models import Band, BandUser
from authentication.serializers import UserSerializer
from authentication.models import User
from rest_framework.exceptions import ValidationError
from authentication.utils import generate_password
from django.core.mail import send_mail
from django.conf import settings
from tours.serializers import TourSerializer


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

        if created:
            password = generate_password()
            user.set_password(password)
            user.save()
            send_mail(
                f"You have been added to {band.name} on indietour",
                f"""Your indietour account has been created and you've been added to {band.name}!
                
Verify your email address so we know it’s really you.
Your email verification code is: {user.verification_code}

You have been assigned a temporary password and recommend you update it upon first login.
Your temporary password is: {password}.

To verify, log in to your account at indietour.app/login and you will be directed to enter your verification code.
""",
                settings.EMAIL_HOST,
                [email],
                fail_silently=False,
            )

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
    tours = TourSerializer(source="tour_set", read_only=True, many=True)
