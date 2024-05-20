#
# Copyright (c) 2020 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of susePublicCloudInfoClient
#
# susePublicCloudInfoClient is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# susePublicCloudInfoClient is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with susePublicCloudInfoClient. If not, see
# <http://www.gnu.org/licenses/>.
#

import json
import re
import requests
import sys
import urllib
from lxml import etree
from typing import Optional, Dict, Any, List, Union



def __apply_filters(superset, filters):
    # map operators to filter functions
    filter_operations = {
        '=': __filter_exact,
        '~': __filter_substring,
        '!': __filter_not_substring,
        '%': __filter_regex,
        '>': __filter_greater_than,
        '<': __filter_less_than
    }
    # prepopulate the result set with all the items
    result_set = superset
    # run through the filters, allowing each to reduce the result set...
    for a_filter in filters:
        result_set = filter_operations[a_filter['operator']](
            result_set,
            a_filter['attr'],
            a_filter['value']
        )
    return result_set


def __filter_exact(items, attr, value):
    """
        select from items list where the attribute is an exact match to 'value'
    """
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if item[attr] == value:
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __filter_substring(items, attr, value):
    """select from items list where 'value' is a substring of the attribute"""
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if value.lower() in item[attr].lower():
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __filter_not_substring(items, attr, value):
    """
        select from items list where 'value' is not a substring of the
        attribute
    """
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if value.lower() not in item[attr].lower():
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __filter_regex(items, attr, value):
    """
        select from items list where 'value' is a regex matching the attribute
    """
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if re.match(value.lower(), item[attr].lower()):
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __filter_less_than(items, attr, value):
    """
        select from items list where the attribute is less than 'value' as
        integers
    """
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if int(item[attr]) < int(value):
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __filter_greater_than(items, attr, value):
    """
        select from items list where the attribute is greater than 'value' as
        integers
    """
    # start with an empty result set
    filtered_items = []
    # iterate over the list of items
    for item in items:
        # append the current item to the result set if matching
        if int(item[attr]) > int(value):
            filtered_items.append(item)
    # return the filtered list
    return filtered_items


def __form_url(framework: Optional[str],
               info_type: str,
               result_format: str = 'xml',
               region: str = 'all',
               image_state: Optional[str] = None,
               server_type: Optional[str] = None,
               apply_filters: Optional[Dict[str, Any]] = None) -> str:
    """
    Form the URL for the request.

    Args:
        framework (Optional[str]): The framework to be used.
        info_type (str): The type of information requested.
        result_format (str, optional): The format of the result, default is 'xml'.
        region (str, optional): The region for the request, default is 'all'.
        image_state (Optional[str], optional): The state of the image, default is None.
        server_type (Optional[str], optional): The type of the server, default is None.
        apply_filters (Optional[Dict[str, Any]], optional): Filters to apply, default is None.

    Returns:
        str: The formed URL.
    """
    url_components = [
        __get_base_url(),
        __get_api_version()
    ]
    
    if framework:
        url_components.append(framework)
    
    region = None if region == 'all' else region
    if region:
        url_components.append(urllib.parse.quote(region))
    
    url_components.append(__map_info_type_to_path(info_type))
    
    doc_type = image_state or server_type
    if doc_type:
        url_components.append(doc_type)
    
    url_components[-1] += '.json'
    url = '/'.join(url_components)
    
    category_query = __get_category_query(info_type)
    if category_query:
        url = f"{url}?{category_query}"
    
    return url

def __map_info_type_to_path(info_type: str) -> str:
    """
    Map the info type to its corresponding path.

    Args:
        info_type (str): The type of information requested.

    Returns:
        str: The mapped path for the given info type.
    """
    mapping = {
        'states': 'images/states',
        'types': 'servers/types',
        'images_version': 'dataversion',
        'servers_version': 'dataversion'
    }
    return mapping.get(info_type, info_type)

def __get_category_query(info_type: str) -> Optional[str]:
    """
    Get the category query string for specific info types.

    Args:
        info_type (str): The type of information requested.

    Returns:
        Optional[str]: The query string if applicable, otherwise None.
    """
    if info_type in ['images_version', 'servers_version']:
        category = 'images' if info_type == 'images_version' else 'servers'
        return urllib.parse.urlencode({'category': category})
    return None

def __get_api_version():
    """Return the API version to use"""
    return 'v1'


def __get_base_url():
    """Return the base url for the information service"""
    return 'https://susepubliccloudinfo.suse.com'
    # return 'http://localhost:9292'


def __get_data(url):
    """Make the request and return the data or None in case of failure"""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        __error("The server responded with an error.\n%s" % e)
    except requests.exceptions.Timeout as e:
        __error("The server did not respond in a timely fashion.\n%s" % e)
    except requests.exceptions.SSLError as e:
        __error(
            "There was a problem with the security of this request:\n%s" % e
        )
    except requests.exceptions.ConnectionError as e:
        __error(
            "There was a problem connecting to the server. "
            "Please check your network connection.\n%s" % e
        )
    except requests.exceptions.RequestException as e:
        __error(e)
    else:
        assert response.text, "No data was returned by the server!"
        return response.text


def __inflect(plural):
    inflections = {
        'images': 'image', 'servers': 'server',
        'providers': 'provider', 'states': 'state', 'types': 'type',
        'regions': 'region'
    }
    return inflections[plural]


def __parse_command_arg_filter(command_arg_filter=None):
    """Break down the --filter argument into a list of filters"""
    valid_filters = {
        'id':
            r'^(?P<attr>id)(?P<operator>[=])(?P<value>.+)$',
        'replacementid':
            r'^(?P<attr>replacementid)(?P<operator>[=])(?P<value>.+)$',
        'ip':
            r'^(?P<attr>ip)(?P<operator>[=])(?P<value>\d+\.\d+\.\d+.\d+)$',
        'name':
            r'^(?P<attr>name)(?P<operator>[~!%])(?P<value>.+)$',
        'replacementname':
            r'(?P<attr>replacementname)(?P<operator>[~!%])(?P<value>.+)$',
        'publishedon':
            r'(?P<attr>publishedon)(?P<operator>[<=>])(?P<value>\d+)$',
        'deprecatedon':
            r'(?P<attr>deprecatedon)(?P<operator>[<=>])(?P<value>\d+)$',
        'deletedon':
            r'(?P<attr>deletedon)(?P<operator>[<=>])(?P<value>\d+)$',
        'type':
            r'^(?P<attr>type)(?P<operator>[~!%])(?P<value>.+)$',
    }
    # start with empty result set
    filters = []
    # split the argument into a comma-separated list if supplied...
    if command_arg_filter:
        for phrase in command_arg_filter.split(','):
            # compare each comma-separated 'phrase' against the valid filters
            # defined by regular expressions
            for attr, regex in list(valid_filters.items()):
                match = re.match(regex, phrase)
                if match:
                    filters.append(match.groupdict())
                    break
            else:
                # if we can't break out with a valid filter, warn the user
                __warn("Invalid filter phrase '%s' will be ignored." % phrase)
    # return any valid filters we found
    return filters


def __parse_server_response_data(server_response_data, info_type):
    if info_type == 'servers_version' or info_type == 'images_version':
        return json.loads(server_response_data)['version']
    
    return json.loads(server_response_data)[info_type]


def __reformat(items: Union[List[Dict[str, Any]], str], 
               info_type: str, 
               result_format: str) -> str:
    """
    Reformat items based on the requested info_type and result_format.

    Args:
        items (Union[List[Dict[str, Any]], str]): The items to be reformatted.
        info_type (str): The type of information.
        result_format (str): The format for the result ('json' or 'xml').

    Returns:
        str: The reformatted string in the desired format.
    """
    if result_format == 'json':
        return json.dumps(
            {info_type: items},
            sort_keys=True,
            indent=2,
            separators=(',', ': ')
        )
    
    if info_type in ['servers_version', 'images_version']:
        root = etree.Element(info_type, attrib={'current_version': items})
        return etree.tostring(
            root,
            xml_declaration=True,
            encoding='UTF-8',
            pretty_print=True
        ).decode()
    
    root = etree.Element(info_type)
    for item in items:
        etree.SubElement(root, __inflect(info_type), item)
    return etree.tostring(
        root,
        xml_declaration=True,
        encoding='UTF-8',
        pretty_print=True
    ).decode()



def __warn(str, out=sys.stdout):
    out.write("Warning: %s\n" % str)


def __error(str, out=sys.stderr):
    out.write("Error: %s\n" % str)
    raise LookupError(str)


def __process(url, info_type, command_arg_filter, result_format):
    """
        given a URL, the type of information, maybe some filters, and an
        expected format, do the right thing
    """
    server_response_data = __get_data(url)
    resultset = __parse_server_response_data(server_response_data, info_type)
    if command_arg_filter:
        filters = __parse_command_arg_filter(command_arg_filter)
        resultset = __apply_filters(resultset, filters)
    return __reformat(resultset, info_type, result_format)


def get_provider_data(
        framework,
        type,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested providers information"""
    info_type = 'providers'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)


def get_image_states_data(
        framework,
        type,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested image states information"""
    info_type = 'states'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)


def get_server_types_data(
        framework,
        type,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested server types information"""
    info_type = 'types'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)


def get_regions_data(
        framework,
        type,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested regions information"""
    info_type = 'regions'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)


def get_image_data(
        framework,
        image_state,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested image information"""
    info_type = 'images'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        image_state,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)


def get_server_data(
        framework,
        server_type,
        result_format='plain',
        region='all',
        command_arg_filter=None):
    """Return the requested server information"""
    info_type = 'servers'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        server_type=server_type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)

def get_servers_version_data(
        framework,
        server_type,
        result_format='plain',
        region='all',
        command_arg_filter=None
    ):
    info_type = 'servers_version'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        server_type=server_type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)

def get_images_version_data(
        framework,
        server_type,
        result_format='plain',
        region='all',
        command_arg_filter=None
    ):
    info_type = 'images_version'
    url = __form_url(
        framework,
        info_type,
        result_format,
        region,
        server_type=server_type,
        apply_filters=command_arg_filter
    )
    return __process(url, info_type, command_arg_filter, result_format)
 