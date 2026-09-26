// Export the interactive Mermaid workflow as two clear, high-resolution layouts.
// Run `npm install` once, then `npm run render:workflow`.

import { existsSync, readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const docs = dirname(fileURLToPath(import.meta.url));
const root = resolve(docs, '..');
const readme = readFileSync(join(root, 'WORKFLOW.md'), 'utf8');
const match = readme.match(/```mermaid\s*\r?\n([\s\S]*?)\r?\n```/);
if (!match) throw new Error('WORKFLOW.md has no Mermaid diagram');

const horizontal = `${match[1].trim()}\n`;
if (!horizontal.startsWith('flowchart LR')) {
  throw new Error('Expected the interactive workflow to start with flowchart LR');
}
const vertical = horizontal
  .replace(/^flowchart LR/m, 'flowchart TB')
  .replace('    subgraph setup', '    subgraph first[" "]\n        direction LR\n    subgraph setup')
  .replace('    subgraph prepare', '    end\n    subgraph second[" "]\n        direction LR\n    subgraph prepare')
  .replace(
    '    setup --> search --> prepare --> outcome',
    '    end\n    setup --> search\n    prepare --> outcome\n    first ~~~ second',
  ) +
  '    style first fill:transparent,stroke:transparent\n' +
  '    style second fill:transparent,stroke:transparent\n';

const layouts = [
  ['horizontal', horizontal],
  ['vertical', vertical],
];
for (const [name, source] of layouts) {
  writeFileSync(join(docs, `workflow-detailed-${name}.mmd`), source);
}

const browserCandidates = [
  process.env.PUPPETEER_EXECUTABLE_PATH,
  process.env.PROGRAMFILES && join(process.env.PROGRAMFILES, 'Google', 'Chrome', 'Application', 'chrome.exe'),
  process.env.PROGRAMFILES && join(process.env.PROGRAMFILES, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
  process.env['PROGRAMFILES(X86)'] && join(process.env['PROGRAMFILES(X86)'], 'Google', 'Chrome', 'Application', 'chrome.exe'),
  process.env.LOCALAPPDATA && join(process.env.LOCALAPPDATA, 'Google', 'Chrome', 'Application', 'chrome.exe'),
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean);
const browser = browserCandidates.find(existsSync);
const configPath = browser ? join(tmpdir(), `getthatjob-puppeteer-${process.pid}.json`) : null;
if (configPath) {
  writeFileSync(configPath, JSON.stringify({ executablePath: browser, args: ['--no-sandbox'] }));
}

const cli = join(root, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');
if (!existsSync(cli)) throw new Error('Run npm install to install Mermaid CLI');

try {
  for (const [name] of layouts) {
    const source = join(docs, `workflow-detailed-${name}.mmd`);
    for (const format of ['svg', 'png']) {
      const target = join(docs, `workflow-detailed-${name}.${format}`);
      const args = [cli, '-i', source, '-o', target, '-b', '#111111', '-s', '4'];
      if (configPath) args.push('-p', configPath);
      const result = spawnSync(process.execPath, args, { cwd: root, stdio: 'inherit' });
      if (result.status !== 0) throw new Error(`Failed to render ${target}`);
      console.log(target);
    }
  }
} finally {
  if (configPath && existsSync(configPath)) unlinkSync(configPath);
}
