#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2020 Cezar H. <https://github.com/usernein>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import pyrogram

from typing import Optional
from pyrogram.types import Identifier, Listener

class GetListenerMatchingWithData:
    def get_listener_matching_with_data(
        self: "pyrogram.Client",
        data: Identifier,
        listener_type: "pyrogram.enums.ListenerTypes"
    ) -> Optional[Listener]:
        """Gets a listener that matches the given data.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            data (:obj:`~pyrogram.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~pyrogram.enums.ListenerTypes`):
                The type of listener to get.

        Returns:
            :obj:`~pyrogram.types.Listener`: On success, a Listener is returned.
        """
        listeners = self.listeners[listener_type]

        if not listeners:
            return None

        matching = []

        # Extract chat_id integers from data for fast pre-filtering
        data_chat_ids = None
        if data.chat_id is not None:
            if isinstance(data.chat_id, list):
                data_chat_ids = {c for c in data.chat_id if isinstance(c, int)}
            elif isinstance(data.chat_id, int):
                data_chat_ids = {data.chat_id}

        for listener in listeners:
            # Fast reject: if both data and listener have integer chat_ids,
            # skip expensive matches() call when they don't overlap
            if data_chat_ids and listener.identifier.chat_id is not None:
                listener_cid = listener.identifier.chat_id
                if isinstance(listener_cid, int):
                    if listener_cid not in data_chat_ids:
                        continue
                elif isinstance(listener_cid, list):
                    listener_int_cids = {c for c in listener_cid if isinstance(c, int)}
                    if listener_int_cids and not listener_int_cids.intersection(data_chat_ids):
                        continue

            if listener.identifier.matches(data):
                matching.append(listener)

        if not matching:
            return None

        # in case of multiple matching listeners, the most specific should be returned
        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes)
