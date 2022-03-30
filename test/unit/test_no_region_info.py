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


def test_global_images_no_regions():
    """Returns empty list for no regions"""
    region_data = '{\n  "regions": []\n}'
    result = ifsrequest.get_regions_data('oracle', None, 'json', 'all', None)
    assert_equals(result, region_data)


def test_images_no_data():
    """Returns empty list for no images"""
    image_data = '{\n  "images": []\n}'
    result = ifsrequest.get_image_data(
        'amazon', None, 'json', 'us-east-1', 'name~foo'
    )
    assert_equals(result, image_data)
