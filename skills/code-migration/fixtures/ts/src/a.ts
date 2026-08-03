// Copyright 2026 Anthropic PBC
// SPDX-License-Identifier: Apache-2.0
import { readFileSync } from "node:fs"; // bare specifier: must NOT appear as an edge
import { b } from "./b"; // edge a -> b (part of the a -> b -> c -> a cycle)
import { u } from "./util"; // edge a -> util/index.ts (directory import resolves to index.ts)

export const a = () => String(b) + String(u) + String(readFileSync);
