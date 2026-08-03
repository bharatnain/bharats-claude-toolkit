# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Fixture package. The `from . import c` below is a relative import from an
__init__.py — it must resolve to pkg/c.py (the package IS the anchor), which
closes the 3-file cycle __init__ -> c -> a -> __init__."""
from . import c  # noqa: F401
