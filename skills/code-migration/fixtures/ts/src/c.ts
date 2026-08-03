// Copyright 2026 Anthropic PBC
// SPDX-License-Identifier: Apache-2.0
const a = require("./a"); // require: edge c -> a (closes the cycle)

export const c = () => a;
