# coding: utf-8

"""
    Strava API v3

    The [Swagger Playground](https://developers.strava.com/playground) is the easiest way to familiarize yourself with the Strava API by submitting HTTP requests and observing the responses before you write any client code. It will show what a response will look like with different endpoints depending on the authorization scope you receive from your athletes. To use the Playground, go to https://www.strava.com/settings/api and change your “Authorization Callback Domain” to developers.strava.com. Please note, we only support Swagger 2.0. There is a known issue where you can only select one scope at a time. For more information, please check the section “client code” at https://developers.strava.com/docs.  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from external.StravaPythonClient.swagger_client.api_client import ApiClient


class SegmentsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def explore_segments(self, bounds, **kwargs):  # noqa: E501
        """Explore segments  # noqa: E501

        Returns the top 10 segments matching a specified query.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.explore_segments(bounds, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[float] bounds: The latitude and longitude for two points describing a rectangular boundary for the search: [southwest corner latitutde, southwest corner longitude, northeast corner latitude, northeast corner longitude] (required)
        :param str activity_type: Desired activity type.
        :param int min_cat: The minimum climbing category.
        :param int max_cat: The maximum climbing category.
        :return: ExplorerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.explore_segments_with_http_info(bounds, **kwargs)  # noqa: E501
        else:
            (data) = self.explore_segments_with_http_info(bounds, **kwargs)  # noqa: E501
            return data

    def explore_segments_with_http_info(self, bounds, **kwargs):  # noqa: E501
        """Explore segments  # noqa: E501

        Returns the top 10 segments matching a specified query.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.explore_segments_with_http_info(bounds, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[float] bounds: The latitude and longitude for two points describing a rectangular boundary for the search: [southwest corner latitutde, southwest corner longitude, northeast corner latitude, northeast corner longitude] (required)
        :param str activity_type: Desired activity type.
        :param int min_cat: The minimum climbing category.
        :param int max_cat: The maximum climbing category.
        :return: ExplorerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['bounds', 'activity_type', 'min_cat', 'max_cat']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method explore_segments" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'bounds' is set
        if ('bounds' not in params or
                params['bounds'] is None):
            raise ValueError("Missing the required parameter `bounds` when calling `explore_segments`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'bounds' in params:
            query_params.append(('bounds', params['bounds']))  # noqa: E501
            collection_formats['bounds'] = 'csv'  # noqa: E501
        if 'activity_type' in params:
            query_params.append(('activity_type', params['activity_type']))  # noqa: E501
        if 'min_cat' in params:
            query_params.append(('min_cat', params['min_cat']))  # noqa: E501
        if 'max_cat' in params:
            query_params.append(('max_cat', params['max_cat']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['strava_oauth']  # noqa: E501

        return self.api_client.call_api(
            '/segments/explore', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplorerResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_logged_in_athlete_starred_segments(self, **kwargs):  # noqa: E501
        """List Starred Segments  # noqa: E501

        List of the authenticated athlete's starred segments. Private segments are filtered out unless requested by a token with read_all scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_logged_in_athlete_starred_segments(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Page number. Defaults to 1.
        :param int per_page: Number of items per page. Defaults to 30.
        :return: list[SummarySegment]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_logged_in_athlete_starred_segments_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_logged_in_athlete_starred_segments_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_logged_in_athlete_starred_segments_with_http_info(self, **kwargs):  # noqa: E501
        """List Starred Segments  # noqa: E501

        List of the authenticated athlete's starred segments. Private segments are filtered out unless requested by a token with read_all scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_logged_in_athlete_starred_segments_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Page number. Defaults to 1.
        :param int per_page: Number of items per page. Defaults to 30.
        :return: list[SummarySegment]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'per_page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_logged_in_athlete_starred_segments" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'per_page' in params:
            query_params.append(('per_page', params['per_page']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['strava_oauth']  # noqa: E501

        return self.api_client.call_api(
            '/segments/starred', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[SummarySegment]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_segment_by_id(self, id, **kwargs):  # noqa: E501
        """Get Segment  # noqa: E501

        Returns the specified segment. read_all scope required in order to retrieve athlete-specific segment information, or to retrieve private segments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_segment_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: The identifier of the segment. (required)
        :return: DetailedSegment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_segment_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_segment_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_segment_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """Get Segment  # noqa: E501

        Returns the specified segment. read_all scope required in order to retrieve athlete-specific segment information, or to retrieve private segments.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_segment_by_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int id: The identifier of the segment. (required)
        :return: DetailedSegment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_segment_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_segment_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['strava_oauth']  # noqa: E501

        return self.api_client.call_api(
            '/segments/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DetailedSegment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def star_segment(self, starred, id, **kwargs):  # noqa: E501
        """Star Segment  # noqa: E501

        Stars/Unstars the given segment for the authenticated athlete. Requires profile:write scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.star_segment(starred, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool starred: (required)
        :param int id: The identifier of the segment to star. (required)
        :return: DetailedSegment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.star_segment_with_http_info(starred, id, **kwargs)  # noqa: E501
        else:
            (data) = self.star_segment_with_http_info(starred, id, **kwargs)  # noqa: E501
            return data

    def star_segment_with_http_info(self, starred, id, **kwargs):  # noqa: E501
        """Star Segment  # noqa: E501

        Stars/Unstars the given segment for the authenticated athlete. Requires profile:write scope.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.star_segment_with_http_info(starred, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool starred: (required)
        :param int id: The identifier of the segment to star. (required)
        :return: DetailedSegment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['starred', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method star_segment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'starred' is set
        if ('starred' not in params or
                params['starred'] is None):
            raise ValueError("Missing the required parameter `starred` when calling `star_segment`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `star_segment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'starred' in params:
            form_params.append(('starred', params['starred']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['strava_oauth']  # noqa: E501

        return self.api_client.call_api(
            '/segments/{id}/starred', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DetailedSegment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
