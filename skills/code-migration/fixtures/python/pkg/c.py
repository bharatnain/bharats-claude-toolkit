# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
import pkg.a  # in-repo: edge c -> pkg/a.py (closes the cycle)


def c():
    return pkg.a.a()
