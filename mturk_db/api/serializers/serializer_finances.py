from rest_framework import serializers


class Serializer_Finances(serializers.Serializer):
    sum_costs_so_far = serializers.IntegerField(default=-1)
    sum_costs_submitted = serializers.IntegerField(default=-1)
    sum_costs_pending = serializers.IntegerField(default=-1)


