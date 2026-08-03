# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
import json  # stdlib: must NOT appear as an edge
from pkg import b  # in-repo: edges a -> pkg/__init__.py and a -> pkg/b.py


def a():
    return json.dumps(b.VALUE)
