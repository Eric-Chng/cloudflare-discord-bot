#!/usr/bin/env node

import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { execFileSync } from 'node:child_process';
import process from 'node:process';

function git(args) {
  return execFileSync('git', args, { encoding: 'utf8' }).trim();
}

let gitDir;

try {
  gitDir = git(['rev-parse', '--git-dir']);
} catch {
  process.exit(0);
}

const hookPath = join(gitDir, 'hooks', 'pre-commit');
const hookBody = `#!/bin/sh

npm run validate:staged-json
`;

mkdirSync(dirname(hookPath), { recursive: true });

if (!existsSync(hookPath)) {
  writeFileSync(hookPath, hookBody, { mode: 0o755 });
}
