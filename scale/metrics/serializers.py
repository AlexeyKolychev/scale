"""Defines the serializers for metrics"""
from __future__ import unicode_literals

import rest_framework.serializers as serializers


class MetricsTypeBaseSerializer(serializers.Serializer):
    """Converts metrics type model fields to REST output"""
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()


class MetricsTypeFilterSerializer(serializers.Serializer):
    """Converts metrics filter model fields to REST output"""
    param = serializers.CharField()
    type = serializers.CharField()


class MetricsTypeColumnSerializer(serializers.Serializer):
    """Converts metrics column model fields to REST output"""
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    units = serializers.CharField()
    group = serializers.CharField()
    aggregate = serializers.CharField()


class MetricsTypeGroupSerializer(serializers.Serializer):
    """Converts metrics group model fields to REST output"""
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()


class MetricsTypeSerializer(serializers.Serializer):
    """Converts metrics type model fields to REST output"""
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    filters = MetricsTypeFilterSerializer(many=True)
    groups = MetricsTypeGroupSerializer(many=True)
    columns = MetricsTypeColumnSerializer(many=True)


class MetricsTypeDetailsSerializer(MetricsTypeSerializer):
    """Converts metrics details model fields to REST output"""
    choices = serializers.CharField()


class MetricsPlotValueSerializer(serializers.Serializer):
    """Converts metrics plot values to REST output"""
    datetime = serializers.DateTimeField()
    value = serializers.IntegerField()
    id = serializers.IntegerField()

    def to_representation(self, obj):
        result = result = super(MetricsPlotValueSerializer, self).to_representation(obj)

        # Not every plotvalue has an 'id' field - remove the empty ones
        if 'id' in result and not result['id']:
            del result['id']
        return result


class MetricsPlotSerializer(serializers.Serializer):
    """Converts metrics plot values to REST output"""
    column = MetricsTypeColumnSerializer()
    min_x = serializers.DateTimeField()
    max_x = serializers.DateTimeField()
    min_y = serializers.IntegerField()
    max_y = serializers.IntegerField()
    values = MetricsPlotValueSerializer(many=True)


class MetricsPlotMultiSerializer(MetricsPlotSerializer):
    """Converts metrics plot values to REST output"""
    values = MetricsPlotValueSerializer(many=True)


class MetricsErrorDetailsSerializer(MetricsTypeDetailsSerializer):
    """Converts ingest metrics details model fields to REST output"""
    from error.serializers import ErrorBaseSerializerV6

    choices = ErrorBaseSerializerV6(many=True)


class MetricsIngestDetailsSerializer(MetricsTypeDetailsSerializer):
    """Converts ingest metrics details model fields to REST output"""
    from ingest.serializers import StrikeBaseSerializer

    choices = StrikeBaseSerializer(many=True)


class MetricsJobTypeDetailsSerializer(MetricsTypeDetailsSerializer):
    """Converts job type metrics details model fields to REST output"""
    from job.job_type_serializers import JobTypeBaseSerializerV6

    choices = JobTypeBaseSerializerV6(many=True)
