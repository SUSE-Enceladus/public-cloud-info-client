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

import unittest
from unittest.mock import patch, MagicMock
from nose.tools import assert_equals

import lib.susepubliccloudinfoclient.infoserverrequests as ifsrequest

class TestGetServersVersionData(unittest.TestCase):

    @patch('lib.susepubliccloudinfoclient.infoserverrequests.__process')
    @patch('lib.susepubliccloudinfoclient.infoserverrequests.__form_url')
    def test_get_servers_version_data(self, mock_form_url, mock_process):
        # Arrange
        mock_form_url.return_value = 'mocked_url'
        mock_process.return_value = 'mocked_response'

        # Act
        result = ifsrequest.get_servers_version_data(
            framework='test_framework',
            server_type='test_server_type',
            result_format='json',
            region='test_region',
            command_arg_filter='test_filter'
        )

        # Assert
        mock_form_url.assert_called_once_with(
            'test_framework',
            'servers_version',
            'json',
            'test_region',
            server_type='test_server_type',
            apply_filters='test_filter'
        )
        mock_process.assert_called_once_with(
            'mocked_url',
            'servers_version',
            'test_filter',
            'json'
        )
        assert_equals(result, 'mocked_response')

    @patch('lib.susepubliccloudinfoclient.infoserverrequests.__process')
    @patch('lib.susepubliccloudinfoclient.infoserverrequests.__form_url')
    def test_get_servers_version_data_default_parameters(self, mock_form_url, mock_process):
        # Arrange
        mock_form_url.return_value = 'mocked_url'
        mock_process.return_value = 'mocked_response'

        # Act
        result = ifsrequest.get_servers_version_data(
            framework='test_framework',
            server_type='test_server_type'
        )

        # Assert
        mock_form_url.assert_called_once_with(
            'test_framework',
            'servers_version',
            'plain',
            'all',
            server_type='test_server_type',
            apply_filters=None
        )
        mock_process.assert_called_once_with(
            'mocked_url',
            'servers_version',
            None,
            'plain'
        )
        assert_equals(result, 'mocked_response')

if __name__ == '__main__':
    unittest.main()