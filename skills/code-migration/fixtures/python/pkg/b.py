# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
import requests  # third-party: must NOT appear as an edge (never executed, only parsed)

VALUE = 2


def b():
    return requests.__name__
