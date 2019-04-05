from rest_framework import serializers


class Serializer_Finances(serializers.Serializer):
    sum_costs_approved = serializers.IntegerField(required=False)
    sum_costs_rejected = serializers.IntegerField(required=False)
    sum_costs_submitted = serializers.IntegerField(required=False)
    sum_costs_dead = serializers.IntegerField(required=False)
    sum_costs_pending = serializers.IntegerField(required=False)

