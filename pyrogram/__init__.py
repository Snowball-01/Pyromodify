#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

__fork_name__ = "pyromodify"
__version__ = "2.3.22"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"

import os
from concurrent.futures.thread import ThreadPoolExecutor
from importlib import import_module


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


__all__ = [
    "__fork_name__",
    "__version__",
    "__license__",
    "__copyright__",
    "StopTransmission",
    "StopPropagation",
    "ContinuePropagation",
    "Client",
    "idle",
    "compose",
    "raw",
    "types",
    "filters",
    "handlers",
    "emoji",
    "enums",
    "crypto_executor",
]

_LAZY_ATTRS = {
    "Client": "pyrogram.client",
    "idle": "pyrogram.sync",
    "compose": "pyrogram.sync",
    "raw": "pyrogram.raw",
    "types": "pyrogram.types",
    "filters": "pyrogram.filters",
    "handlers": "pyrogram.handlers",
    "emoji": "pyrogram.emoji",
    "enums": "pyrogram.enums",
}


def __getattr__(name):
    module_path = _LAZY_ATTRS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(module_path)
    if name in {"raw", "types", "filters", "handlers", "emoji", "enums"}:
        value = module
    else:
        value = getattr(module, name)

    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals().keys()) | set(_LAZY_ATTRS.keys()))


crypto_executor = ThreadPoolExecutor(
    min(4, os.cpu_count() or 1), thread_name_prefix="CryptoWorker"
)
