# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class DeletePermissionsByFilterTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()
        self.permission_mock_xml = f'''
            <get_permissions_response status="200" status_text="OK">
            <permission id="{self.id1}">
                <owner>
                <name>myuser</name>
                </owner>
                <name>get_tasks</name>
                <comment/>
                <creation_time>2020-11-09T09:44:23Z</creation_time>
                <modification_time>2020-11-09T09:44:23Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <resource id="df479236-1803-4e46-9014-2981ba9e15b1">
                <name>task Clone 1</name>
                <type>task</type>
                <trash>0</trash>
                <deleted>0</deleted>
                </resource>
                <subject id="f8d47c31-e63f-4d3b-a5e8-0aa2f56ba2a0">
                <name>myuser</name>
                <type>user</type>
                <trash>0</trash>
                </subject>
            </permission>
            <permission id="{self.id2}">
                <owner>
                <name>myuser</name>
                </owner>
                <name>create_agent</name>
                <comment/>
                <creation_time>2020-11-09T09:44:23Z</creation_time>
                <modification_time>2020-11-09T09:44:23Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <resource id="df479236-1803-4e46-9014-2981ba9e15b1">
                <name>task Clone 1</name>
                <type>task</type>
                <trash>0</trash>
                <deleted>0</deleted>
                </resource>
                <subject id="f8d47c31-e63f-4d3b-a5e8-0aa2f56ba2a0">
                <name>myuser</name>
                <type>user</type>
                <trash>0</trash>
                </subject>
            </permission>
            </get_permissions_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deletePermissionsByFilter(
                    filterString:"name~create_agent",
                    ultimate: false)
                {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_permissions_by_filter(self, mock_gmp: GmpMockFactory):

        self.login('foo', 'bar')

        mock_gmp.mock_response('get_permissions', self.permission_mock_xml)

        response = self.query(
            '''
            mutation {
                deletePermissionsByFilter(
                    filterString:"name~create_agent",
                    ultimate: false)
                {
                   ok
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deletePermissionsByFilter']['ok']
        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_permissions.assert_called_with(
            filter_string="name~create_agent"
        )

        mock_gmp.gmp_protocol.delete_permission.assert_called_with(
            f'{self.id2}'
        )
