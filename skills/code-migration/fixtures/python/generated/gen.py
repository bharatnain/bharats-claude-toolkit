# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Lives in generated/, which is excluded by SKIP_DIRS in depmap_python.py.
# This file (and its import) must not appear in edges.tsv, order.txt, or cycles.txt.
import pkg.a  # noqa: F401
