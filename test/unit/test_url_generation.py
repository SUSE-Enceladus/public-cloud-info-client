#!/usr/bin/python
#
# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
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

import lib.susepubliccloudinfoclient.infoserverrequests as ifsrequest
from nose.tools import assert_equals


def test_api_version():
    assert_equals('v1', ifsrequest.__get_api_version())


def test_get_base_url():
    expected = 'https://susepubliccloudinfo.suse.com'
    assert_equals(expected, ifsrequest.__get_base_url())


def test_form_url_servers_all_json():
    """Form the URL for all servers in JSON format"""
    url = ifsrequest.__form_url('amazon', 'servers', 'json')
    expected = 'https://susepubliccloudinfo.suse.com/v1/amazon/servers.json'
    assert_equals(expected, url)


def test_form_url_servers_smt_xml():
    """Form the URL for all SMT servers in XML"""
    url = ifsrequest.__form_url('google', 'servers', server_type='smt')
    # all requests are in JSON, regardless of output format
    expected = (
        'https://susepubliccloudinfo.suse.com'
        '/v1/google/servers/smt.json'
    )
    assert_equals(expected, url)


def test_form_url_images_active_region_json():
    """Form the URL for active images in JSON format in a given region"""
    url = ifsrequest.__form_url(
        'amazon',
        'images',
        result_format='json',
        region='us-east-1',
        image_state='active')
    expected = 'https://susepubliccloudinfo.suse.com/v1/'
    expected += 'amazon/us-east-1/images/active.json'
    assert_equals(expected, url)


def test_form_url_images_inactive():
    """Form URL for inactive images (defaults to JSON)"""
    url = ifsrequest.__form_url(
        'microsoft',
        'images',
        image_state='inactive')
    expected = (
        'https://susepubliccloudinfo.suse.com/v1/'
        'microsoft/images/inactive.json')
    assert_equals(expected, url)


def test_form_url_images_all_xml():
    """Form URL for all images in XML format"""
    url = ifsrequest.__form_url('google', 'images')
    # all requests are in JSON, regardless of output format
    expected = 'https://susepubliccloudinfo.suse.com/v1/google/images.json'
    assert_equals(expected, url)


def test_region_is_url_quoted():
    """Region may contain spaces; it should be URL quoted"""
    url = ifsrequest.__form_url('microsoft', 'images', region='West US')
    expected = (
        'https://susepubliccloudinfo.suse.com'
        '/v1/microsoft/West%20US/images.json'
    )
    assert_equals(expected, url)


def test_all_frameworks():
    """As new frameworks are added, we smoketest the values"""
    frameworks = ['amazon', 'google', 'microsoft', 'oracle']
    for framework in frameworks:
        url = ifsrequest.__form_url(framework, 'images', region='dummy')
        expected = (
            'https://susepubliccloudinfo.suse.com'
            '/v1/' + framework + '/dummy/images.json'
        )
        assert_equals(expected, url)


def test_form_url_providers_xml():
    """Form the URL for all providers in XML"""
    url = ifsrequest.__form_url('', 'providers')
    # all requests are in JSON, regardless of output format
    expected = (
        'https://susepubliccloudinfo.suse.com'
        '/v1/providers.json'
    )
    assert_equals(expected, url)


def test_form_url_images_states():
    """Form URL for image states (defaults to JSON)"""
    url = ifsrequest.__form_url('', 'states')
    expected = (
        'https://susepubliccloudinfo.suse.com/v1/'
        'images/states.json')
    assert_equals(expected, url)


def test_form_url_servers_types():
    """Form URL for servers types (defaults to JSON)"""
    url = ifsrequest.__form_url(
        'microsoft',
        'types')
    expected = (
        'https://susepubliccloudinfo.suse.com/v1/'
        'microsoft/servers/types.json')
    assert_equals(expected, url)


def test_form_url_regions():
    """Form URL for regions list (defaults to JSON)"""
    url = ifsrequest.__form_url(
        'amazon',
        'regions')
    expected = (
        'https://susepubliccloudinfo.suse.com/v1/'
        'amazon/regions.json')
    assert_equals(expected, url)

def test_form_url_servers_version():
    """Given the servers_version info_type when forming URL then correctly forms the url with query parameters"""
    url = ifsrequest.__form_url(
        'amazon',
        'servers_version'
    )
    expected = (
       'https://susepubliccloudinfo.suse.com/v1/'
        'amazon/dataversion.json?category=servers'        
    )
    assert_equals(expected, url)
    
def test_form_url_images_version():
    """Given the images_version info_type when forming URL then correctly forms the url with query parameters"""
    url = ifsrequest.__form_url(
        'amazon',
        'images_version'
    )
    expected = (
       'https://susepubliccloudinfo.suse.com/v1/'
        'amazon/dataversion.json?category=images'        
    )
    assert_equals(expected, url)