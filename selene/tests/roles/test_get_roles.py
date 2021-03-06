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

# pylint: disable=line-too-long

from uuid import uuid4

from unittest.mock import patch

from selene.tests import SeleneTestCase, GmpMockFactory
from selene.tests.entity import make_test_get_entities


@patch('selene.views.Gmp', new_callable=GmpMockFactory)
class GetRolesTestCase(SeleneTestCase):
    def setUp(self):
        self.id1 = uuid4()
        self.id2 = uuid4()
        self.resp = f'''
            <get_roles_response status="200" status_text="OK">
            <role id="{self.id1}">
                <owner>
                    <name>myuser</name>
                </owner>
                <name>test1</name>
                <comment>test</comment>
                <creation_time>2020-09-04T12:53:52Z</creation_time>
                <modification_time>2020-11-10T13:19:36Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <users>hyperion_test_user, myuser</users>
            </role>
            <role id="{self.id2}">
                <owner>
                    <name>myuser</name>
                </owner>
                <name>test2</name>
                <comment>test</comment>
                <creation_time>2020-09-04T12:53:52Z</creation_time>
                <modification_time>2020-11-10T13:19:36Z</modification_time>
                <writable>1</writable>
                <in_use>0</in_use>
                <permissions>
                <permission>
                    <name>Everything</name>
                </permission>
                </permissions>
                <users>hyperion_test_user, myuser</users>
            </role>
            </get_roles_response>
            '''

    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            query {
                roles{
                    nodes {
                        id
                        name
                        users
                    }
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_get_roles(self, mock_gmp: GmpMockFactory):
        mock_gmp.mock_response('get_roles', self.resp)

        self.login('foo', 'bar')

        response = self.query(
            '''
            query {
                roles{
                    nodes {
                        id
                        name
                        users
                    }
                }
            }
            '''
        )

        json = response.json()

        self.assertResponseNoErrors(response)

        roles = json['data']['roles']['nodes']

        self.assertEqual(len(roles), 2)

        role1 = roles[0]
        role2 = roles[1]

        # Role 1
        self.assertEqual(role1['name'], 'test1')
        self.assertEqual(role1['id'], f'{self.id1}')
        self.assertEqual(role1['users'], ['hyperion_test_user', 'myuser'])

        # Role 2
        self.assertEqual(role2['name'], 'test2')
        self.assertEqual(role2['id'], f'{self.id2}')
        self.assertEqual(role2['users'], ['hyperion_test_user', 'myuser'])

        mock_gmp.gmp_protocol.get_roles.assert_called_with(filter_string=None)


class RolesGetEntitiesTestCase(SeleneTestCase):
    gmp_name = 'role'
    selene_name = 'role'
    test_get_entities = make_test_get_entities(
        gmp_name, selene_name=selene_name
    )
