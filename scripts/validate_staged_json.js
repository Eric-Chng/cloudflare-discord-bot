#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import process from 'node:process';

function git(args) {
  return execFileSync('git', args, { encoding: 'utf8' });
}

function stagedJsonFiles() {
  const output = git([
    'diff',
    '--cached',
    '--name-only',
    '--diff-filter=ACMR',
    '-z',
    '--',
    '*.json',
  ]);

  return output.split('\0').filter(Boolean);
}

function stagedFileContents(file) {
  return git(['show', `:${file}`]);
}

const failures = [];

for (const file of stagedJsonFiles()) {
  try {
    JSON.parse(stagedFileContents(file));
  } catch (error) {
    failures.push({ file, message: error.message });
  }
}

if (failures.length > 0) {
  console.error('Invalid JSON in staged files:');

  for (const failure of failures) {
    console.error(`- ${failure.file}: ${failure.message}`);
  }

  process.exit(1);
}
