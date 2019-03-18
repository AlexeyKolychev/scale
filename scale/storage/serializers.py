"""Defines the serializers for Scale files and workspaces"""
from __future__ import unicode_literals

import rest_framework.serializers as serializers
from rest_framework.fields import CharField

from util.rest import ModelIdSerializer


class WktField(CharField):
    """Field for displaying geometry objects as Well Known Text"""

    type_name = 'WktField'
    type_label = 'wtk'

    def to_representation(self, value):
        """Converts the model field to WKT

        :param value: the associated geometry info
        :type value: GEOSGeometry
        :rtype: string
        :returns: the WKT representation
        """
        if value:
            return value.wkt


class GeoJsonField(CharField):
    """Field for displaying geometry objects as Well Known Text"""

    type_name = 'GeoJsonField'
    type_label = 'geojson'

    def to_representation(self, value):
        """Converts the model field to GeoJson

        :param value: the associated geometry info
        :type value: GEOSGeometry
        :rtype: string
        :returns: the GeoJson representation
        """
        if value:
            return value.geojson


class WorkspaceBaseSerializer(ModelIdSerializer):
    """Converts workspace model fields to REST output"""
    name = serializers.CharField()


class WorkspaceSerializerV5(WorkspaceBaseSerializer):
    """Converts workspace model fields to REST output"""
    title = serializers.CharField()
    description = serializers.CharField()
    base_url = serializers.URLField()
    is_active = serializers.BooleanField()

    used_size = serializers.IntegerField(source='zero_size')
    total_size = serializers.IntegerField(source='zero_size')

    created = serializers.DateTimeField()
    archived = serializers.DateTimeField(source='deprecated')
    last_modified = serializers.DateTimeField()


class WorkspaceDetailsSerializerV5(WorkspaceSerializerV5):
    """Converts workspace model fields to REST output"""
    json_config = serializers.JSONField(default=dict)

class WorkspaceSerializerV6(WorkspaceBaseSerializer):
    """Converts workspace model fields to REST output"""
    title = serializers.CharField()
    description = serializers.CharField()
    base_url = serializers.URLField()
    is_active = serializers.BooleanField()

    created = serializers.DateTimeField()
    deprecated = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()


class WorkspaceDetailsSerializerV6(WorkspaceSerializerV6):
    """Converts workspace model fields to REST output"""
    configuration = serializers.JSONField(source='get_v6_configuration_json')

class ScaleFileBaseSerializerV5(ModelIdSerializer):
    """Converts Scale file model fields to REST output"""
    workspace = WorkspaceBaseSerializer()

    file_name = serializers.CharField()
    media_type = serializers.CharField()
    file_type = serializers.CharField()
    file_size = serializers.IntegerField()  # TODO: BigIntegerField?
    data_type_tags = serializers.CharField(many=true)
    is_deleted = serializers.BooleanField()
    uuid = serializers.CharField()
    url = serializers.URLField()

    created = serializers.DateTimeField()
    deleted = serializers.DateTimeField()
    data_started = serializers.DateTimeField()
    data_ended = serializers.DateTimeField()
    source_started = serializers.DateTimeField()
    source_ended = serializers.DateTimeField()

    last_modified = serializers.DateTimeField()
    
class ScaleFileBaseSerializerV6(ModelIdSerializer):
    """Converts Scale file model fields to REST output"""

    file_name = serializers.CharField()


class ScaleFileSerializerV5(ScaleFileBaseSerializerV5):
    """Converts Scale file model fields to REST output"""

    file_path = serializers.CharField()

    # TODO: update to use GeoJson instead of WKT
    geometry = WktField()
    center_point = WktField()
    meta_data = serializers.JSONField(default=dict)
    countries = serializers.StringRelatedField(many=True, read_only=True)
    
class ScaleFileSerializerV6(ScaleFileBaseSerializerV6):
    """Converts Scale file model fields to REST output"""
    from batch.serializers import BatchBaseSerializerV6
    from job.job_type_serializers import JobTypeBaseSerializerV6
    from recipe.serializers import RecipeTypeBaseSerializerV6

    workspace = WorkspaceBaseSerializer()
    media_type = serializers.CharField()
    file_type = serializers.CharField()
    file_size = serializers.IntegerField()  # TODO: BigIntegerField?
    file_path = serializers.CharField()
    is_deleted = serializers.BooleanField()
    url = serializers.URLField()

    created = serializers.DateTimeField()
    deleted = serializers.DateTimeField()
    data_started = serializers.DateTimeField()
    data_ended = serializers.DateTimeField()
    source_started = serializers.DateTimeField()
    source_ended = serializers.DateTimeField()
    source_sensor_class = serializers.CharField()
    source_sensor = serializers.CharField()
    source_collection = serializers.CharField()
    source_task = serializers.CharField()
    last_modified = serializers.DateTimeField()
    # TODO: update to use GeoJson instead of WKT
    geometry = WktField()
    center_point = WktField()
    countries = serializers.StringRelatedField(many=True, read_only=True)

    job_type = JobTypeBaseSerializerV6()
    job = ModelIdSerializer()
    job_exe = ModelIdSerializer()
    job_output = serializers.CharField()

    recipe_type = RecipeTypeBaseSerializerV6()
    recipe = ModelIdSerializer()
    recipe_node = serializers.CharField()
    batch = BatchBaseSerializerV6()

    is_superseded = serializers.BooleanField()
    superseded = serializers.DateTimeField()


class ScaleFileDetailsSerializerV6(ScaleFileSerializerV6):
    """Converts file model fields to REST output"""
    
    meta_data = serializers.JSONField(default=dict)
