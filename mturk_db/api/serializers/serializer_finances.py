from rest_framework import serializers


class Serializer_Finances(serializers.Serializer):
    sum_costs_max = serializers.IntegerField()
    sum_costs_so_far = serializers.IntegerField()


