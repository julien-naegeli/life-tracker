# coding: utf-8

# flake8: noqa
"""
    Strava API v3

    The [Swagger Playground](https://developers.strava.com/playground) is the easiest way to familiarize yourself with the Strava API by submitting HTTP requests and observing the responses before you write any client code. It will show what a response will look like with different endpoints depending on the authorization scope you receive from your athletes. To use the Playground, go to https://www.strava.com/settings/api and change your “Authorization Callback Domain” to developers.strava.com. Please note, we only support Swagger 2.0. There is a known issue where you can only select one scope at a time. For more information, please check the section “client code” at https://developers.strava.com/docs.  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from external.StravaPythonClient.swagger_client.models.activities_body import ActivitiesBody
from external.StravaPythonClient.swagger_client.models.activity_stats import ActivityStats
from external.StravaPythonClient.swagger_client.models.activity_total import ActivityTotal
from external.StravaPythonClient.swagger_client.models.activity_type import ActivityType
from external.StravaPythonClient.swagger_client.models.activity_zone import ActivityZone
from external.StravaPythonClient.swagger_client.models.altitude_stream import AltitudeStream
from external.StravaPythonClient.swagger_client.models.base_stream import BaseStream
from external.StravaPythonClient.swagger_client.models.cadence_stream import CadenceStream
from external.StravaPythonClient.swagger_client.models.club_activity import ClubActivity
from external.StravaPythonClient.swagger_client.models.club_athlete import ClubAthlete
from external.StravaPythonClient.swagger_client.models.comment import Comment
from external.StravaPythonClient.swagger_client.models.detailed_activity import DetailedActivity
from external.StravaPythonClient.swagger_client.models.detailed_athlete import DetailedAthlete
from external.StravaPythonClient.swagger_client.models.detailed_club import DetailedClub
from external.StravaPythonClient.swagger_client.models.detailed_gear import DetailedGear
from external.StravaPythonClient.swagger_client.models.detailed_segment import DetailedSegment
from external.StravaPythonClient.swagger_client.models.detailed_segment_effort import DetailedSegmentEffort
from external.StravaPythonClient.swagger_client.models.distance_stream import DistanceStream
from external.StravaPythonClient.swagger_client.models.error import Error
from external.StravaPythonClient.swagger_client.models.explorer_response import ExplorerResponse
from external.StravaPythonClient.swagger_client.models.explorer_segment import ExplorerSegment
from external.StravaPythonClient.swagger_client.models.fault import Fault
from external.StravaPythonClient.swagger_client.models.heart_rate_zone_ranges import HeartRateZoneRanges
from external.StravaPythonClient.swagger_client.models.heartrate_stream import HeartrateStream
from external.StravaPythonClient.swagger_client.models.id_starred_body import IdStarredBody
from external.StravaPythonClient.swagger_client.models.lap import Lap
from external.StravaPythonClient.swagger_client.models.lat_lng import LatLng
from external.StravaPythonClient.swagger_client.models.lat_lng_stream import LatLngStream
from external.StravaPythonClient.swagger_client.models.meta_activity import MetaActivity
from external.StravaPythonClient.swagger_client.models.meta_athlete import MetaAthlete
from external.StravaPythonClient.swagger_client.models.meta_club import MetaClub
from external.StravaPythonClient.swagger_client.models.moving_stream import MovingStream
from external.StravaPythonClient.swagger_client.models.photos_summary import PhotosSummary
from external.StravaPythonClient.swagger_client.models.photos_summary_primary import PhotosSummaryPrimary
from external.StravaPythonClient.swagger_client.models.polyline_map import PolylineMap
from external.StravaPythonClient.swagger_client.models.power_stream import PowerStream
from external.StravaPythonClient.swagger_client.models.power_zone_ranges import PowerZoneRanges
from external.StravaPythonClient.swagger_client.models.route import Route
from external.StravaPythonClient.swagger_client.models.smooth_grade_stream import SmoothGradeStream
from external.StravaPythonClient.swagger_client.models.smooth_velocity_stream import SmoothVelocityStream
from external.StravaPythonClient.swagger_client.models.split import Split
from external.StravaPythonClient.swagger_client.models.sport_type import SportType
from external.StravaPythonClient.swagger_client.models.stream_set import StreamSet
from external.StravaPythonClient.swagger_client.models.summary_activity import SummaryActivity
from external.StravaPythonClient.swagger_client.models.summary_athlete import SummaryAthlete
from external.StravaPythonClient.swagger_client.models.summary_club import SummaryClub
from external.StravaPythonClient.swagger_client.models.summary_gear import SummaryGear
from external.StravaPythonClient.swagger_client.models.summary_pr_segment_effort import SummaryPRSegmentEffort
from external.StravaPythonClient.swagger_client.models.summary_segment import SummarySegment
from external.StravaPythonClient.swagger_client.models.summary_segment_effort import SummarySegmentEffort
from external.StravaPythonClient.swagger_client.models.temperature_stream import TemperatureStream
from external.StravaPythonClient.swagger_client.models.time_stream import TimeStream
from external.StravaPythonClient.swagger_client.models.timed_zone_distribution import TimedZoneDistribution
from external.StravaPythonClient.swagger_client.models.timed_zone_range import TimedZoneRange
from external.StravaPythonClient.swagger_client.models.updatable_activity import UpdatableActivity
from external.StravaPythonClient.swagger_client.models.upload import Upload
from external.StravaPythonClient.swagger_client.models.uploads_body import UploadsBody
from external.StravaPythonClient.swagger_client.models.zone_range import ZoneRange
from external.StravaPythonClient.swagger_client.models.zone_ranges import ZoneRanges
from external.StravaPythonClient.swagger_client.models.zones import Zones
