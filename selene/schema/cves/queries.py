# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Greenbone Networks GmbH
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

import graphene

from graphql import ResolveInfo
from gvm.protocols.next import InfoType as GvmInfoType

from selene.schema.cves.fields import CVE

from selene.schema.parser import FilterString

from selene.schema.relay import (
    EntityConnectionField,
    Entities,
    get_filter_string_for_pagination,
)

from selene.schema.utils import get_gmp, require_authentication, XmlElement


class GetCVE(graphene.Field):
    """Gets a single CVE information.

    Args:
        id (str): ID of the CVE information being queried

    Example:

        .. code-block::

            query {
                cve (id: "CVE-2020-12345"){
                        id
                        name
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cve": {
                        "id": "CVE-2020-12345",
                        "name": "foo"
                    }
                }
            }

    """

    def __init__(self):
        super().__init__(
            CVE,
            cve_id=graphene.String(required=True, name='id'),
            resolver=self.resolve,
        )

    @staticmethod
    @require_authentication
    def resolve(_root, info, cve_id: str):
        gmp = get_gmp(info)

        xml = gmp.get_info(str(cve_id), info_type=GvmInfoType.CVE)
        return xml.find('info')


class GetCVEs(EntityConnectionField):
    """Gets a list of CVE information with pagination

    Args:
        filter_string (str, optional): Optional filter string to be
            used with query.

    Example:

        .. code-block::

            query {
                cves (filterString: "name~Foo rows=2") {
                    nodes {
                        id
                        name
                    }
                }
            }

        Response:

        .. code-block::

            {
                "data": {
                    "cves": {
                        "nodes": [
                            {
                                "id": "CVE-2020-12345",
                                "name": "Foo"
                            },
                            {
                                "id": "CVE-2020-12346",
                                "name": "Foo Bar"
                            },
                        ]
                    }
                }
            }

    """

    entity_type = CVE

    @staticmethod
    @require_authentication
    def resolve_entities(  # pylint: disable=arguments-differ
        _root,
        info: ResolveInfo,
        filter_string: FilterString = None,
        after: str = None,
        before: str = None,
        first: int = None,
        last: int = None,
    ) -> Entities:
        gmp = get_gmp(info)

        filter_string = get_filter_string_for_pagination(
            filter_string, first=first, last=last, after=after, before=before
        )

        xml: XmlElement = gmp.get_info_list(
            filter_string=filter_string.filter_string, info_type=GvmInfoType.CVE
        )

        requested = None
        cve_elements = []
        info_elements = xml.findall('info')
        for element in info_elements:
            if element.get('id'):
                cve_elements.append(element)
            else:
                requested = element
        counts = xml.find('info_count')

        return Entities(cve_elements, counts, requested)
