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
class DeletePortListsByIdsTestCase(SeleneTestCase):
    def test_require_authentication(self, _mock_gmp: GmpMockFactory):
        response = self.query(
            '''
            mutation {
                deletePortListsByIds(
                    ids: ["e1438fb2-ab2c-4f4a-ad6b-de97005256e8"]
                ) {
                   ok
                }
            }
            '''
        )

        self.assertResponseAuthenticationRequired(response)

    def test_delete_port_lists(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        mock_gmp.mock_response(
            'get_port_lists',
            f'''
            <get_port_lists_response status="200" status_text="OK">
                <port_list id="{id1}">
                    <name>Foo Clone 1</name>
                </port_list>
                <port_list id="{id2}">
                    <name>Foo Clone 2</name>
                </port_list>
            </get_port_lists_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deletePortListsByIds(ids: ["{id1}", "{id2}"]) {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deletePortListsByIds']['ok']

        self.assertTrue(ok)

        mock_gmp.gmp_protocol.get_port_lists.assert_called_with(
            filter_string=f'uuid={id1} uuid={id2} '
        )

        mock_gmp.gmp_protocol.delete_port_list.assert_any_call(
            port_list_id=str(id1)
        )

        mock_gmp.gmp_protocol.delete_port_list.assert_any_call(
            port_list_id=str(id2)
        )

    def test_delete_port_lists_invalid(self, mock_gmp: GmpMockFactory):
        self.login('foo', 'bar')

        id1 = uuid4()
        id2 = uuid4()

        # Only one of the requested port_lists is found.
        mock_gmp.mock_response(
            'get_port_lists',
            f'''
            <get_port_lists_response status="200" status_text="OK">
                <port_list id="{id1}">
                    <name>Foo Clone 1</name>
                </port_list>
            </get_port_lists_response>
            ''',
        )

        response = self.query(
            f'''
            mutation {{
                deletePortListsByIds(ids: ["{id1}", "{id2}"]) {{
                    ok
                }}
            }}
            '''
        )
        json = response.json()

        self.assertResponseNoErrors(response)

        ok = json['data']['deletePortListsByIds']['ok']

        self.assertFalse(ok)

        mock_gmp.gmp_protocol.get_port_lists.assert_called_with(
            filter_string=f'uuid={id1} uuid={id2} '
        )
