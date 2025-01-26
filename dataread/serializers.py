from rest_framework import serializers
from .models import Users,Competition

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'manager',  'real_name']
class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id','year','name','competition_level','award_level','leader_name','leader_id','member_name','is_guoyuan']