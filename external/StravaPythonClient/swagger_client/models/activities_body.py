# coding: utf-8

"""
    Strava API v3

    The [Swagger Playground](https://developers.strava.com/playground) is the easiest way to familiarize yourself with the Strava API by submitting HTTP requests and observing the responses before you write any client code. It will show what a response will look like with different endpoints depending on the authorization scope you receive from your athletes. To use the Playground, go to https://www.strava.com/settings/api and change your “Authorization Callback Domain” to developers.strava.com. Please note, we only support Swagger 2.0. There is a known issue where you can only select one scope at a time. For more information, please check the section “client code” at https://developers.strava.com/docs.  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ActivitiesBody(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'type': 'str',
        'sport_type': 'str',
        'start_date_local': 'datetime',
        'elapsed_time': 'int',
        'description': 'str',
        'distance': 'float',
        'trainer': 'int',
        'commute': 'int'
    }

    attribute_map = {
        'name': 'name',
        'type': 'type',
        'sport_type': 'sport_type',
        'start_date_local': 'start_date_local',
        'elapsed_time': 'elapsed_time',
        'description': 'description',
        'distance': 'distance',
        'trainer': 'trainer',
        'commute': 'commute'
    }

    def __init__(self, name=None, type=None, sport_type=None, start_date_local=None, elapsed_time=None, description=None, distance=None, trainer=None, commute=None):  # noqa: E501
        """ActivitiesBody - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._type = None
        self._sport_type = None
        self._start_date_local = None
        self._elapsed_time = None
        self._description = None
        self._distance = None
        self._trainer = None
        self._commute = None
        self.discriminator = None
        self.name = name
        if type is not None:
            self.type = type
        self.sport_type = sport_type
        self.start_date_local = start_date_local
        self.elapsed_time = elapsed_time
        if description is not None:
            self.description = description
        if distance is not None:
            self.distance = distance
        if trainer is not None:
            self.trainer = trainer
        if commute is not None:
            self.commute = commute

    @property
    def name(self):
        """Gets the name of this ActivitiesBody.  # noqa: E501

        The name of the activity.  # noqa: E501

        :return: The name of this ActivitiesBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ActivitiesBody.

        The name of the activity.  # noqa: E501

        :param name: The name of this ActivitiesBody.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this ActivitiesBody.  # noqa: E501

        Type of activity. For example - Run, Ride etc.  # noqa: E501

        :return: The type of this ActivitiesBody.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ActivitiesBody.

        Type of activity. For example - Run, Ride etc.  # noqa: E501

        :param type: The type of this ActivitiesBody.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def sport_type(self):
        """Gets the sport_type of this ActivitiesBody.  # noqa: E501

        Sport type of activity. For example - Run, MountainBikeRide, Ride, etc.  # noqa: E501

        :return: The sport_type of this ActivitiesBody.  # noqa: E501
        :rtype: str
        """
        return self._sport_type

    @sport_type.setter
    def sport_type(self, sport_type):
        """Sets the sport_type of this ActivitiesBody.

        Sport type of activity. For example - Run, MountainBikeRide, Ride, etc.  # noqa: E501

        :param sport_type: The sport_type of this ActivitiesBody.  # noqa: E501
        :type: str
        """
        if sport_type is None:
            raise ValueError("Invalid value for `sport_type`, must not be `None`")  # noqa: E501

        self._sport_type = sport_type

    @property
    def start_date_local(self):
        """Gets the start_date_local of this ActivitiesBody.  # noqa: E501

        ISO 8601 formatted date time.  # noqa: E501

        :return: The start_date_local of this ActivitiesBody.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date_local

    @start_date_local.setter
    def start_date_local(self, start_date_local):
        """Sets the start_date_local of this ActivitiesBody.

        ISO 8601 formatted date time.  # noqa: E501

        :param start_date_local: The start_date_local of this ActivitiesBody.  # noqa: E501
        :type: datetime
        """
        if start_date_local is None:
            raise ValueError("Invalid value for `start_date_local`, must not be `None`")  # noqa: E501

        self._start_date_local = start_date_local

    @property
    def elapsed_time(self):
        """Gets the elapsed_time of this ActivitiesBody.  # noqa: E501

        In seconds.  # noqa: E501

        :return: The elapsed_time of this ActivitiesBody.  # noqa: E501
        :rtype: int
        """
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, elapsed_time):
        """Sets the elapsed_time of this ActivitiesBody.

        In seconds.  # noqa: E501

        :param elapsed_time: The elapsed_time of this ActivitiesBody.  # noqa: E501
        :type: int
        """
        if elapsed_time is None:
            raise ValueError("Invalid value for `elapsed_time`, must not be `None`")  # noqa: E501

        self._elapsed_time = elapsed_time

    @property
    def description(self):
        """Gets the description of this ActivitiesBody.  # noqa: E501

        Description of the activity.  # noqa: E501

        :return: The description of this ActivitiesBody.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ActivitiesBody.

        Description of the activity.  # noqa: E501

        :param description: The description of this ActivitiesBody.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def distance(self):
        """Gets the distance of this ActivitiesBody.  # noqa: E501

        In meters.  # noqa: E501

        :return: The distance of this ActivitiesBody.  # noqa: E501
        :rtype: float
        """
        return self._distance

    @distance.setter
    def distance(self, distance):
        """Sets the distance of this ActivitiesBody.

        In meters.  # noqa: E501

        :param distance: The distance of this ActivitiesBody.  # noqa: E501
        :type: float
        """

        self._distance = distance

    @property
    def trainer(self):
        """Gets the trainer of this ActivitiesBody.  # noqa: E501

        Set to 1 to mark as a trainer activity.  # noqa: E501

        :return: The trainer of this ActivitiesBody.  # noqa: E501
        :rtype: int
        """
        return self._trainer

    @trainer.setter
    def trainer(self, trainer):
        """Sets the trainer of this ActivitiesBody.

        Set to 1 to mark as a trainer activity.  # noqa: E501

        :param trainer: The trainer of this ActivitiesBody.  # noqa: E501
        :type: int
        """

        self._trainer = trainer

    @property
    def commute(self):
        """Gets the commute of this ActivitiesBody.  # noqa: E501

        Set to 1 to mark as commute.  # noqa: E501

        :return: The commute of this ActivitiesBody.  # noqa: E501
        :rtype: int
        """
        return self._commute

    @commute.setter
    def commute(self, commute):
        """Sets the commute of this ActivitiesBody.

        Set to 1 to mark as commute.  # noqa: E501

        :param commute: The commute of this ActivitiesBody.  # noqa: E501
        :type: int
        """

        self._commute = commute

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ActivitiesBody, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ActivitiesBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
