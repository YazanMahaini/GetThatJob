// Render the detailed GetThatJob decision flow in both reading directions.
// Run `npm install` once, then `npm run render:workflow`.

import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { instance } from '@viz-js/viz';

const here = dirname(fileURLToPath(import.meta.url));
const nodes = [
  ['start', 'Ask GetThatJob for help'],
  ['first', 'First use in this workspace?', true],
  ['setup', 'SetupSkill creates missing folders\nand blank tracking files'],
  ['check', 'SetupChecker checks what is available'],
  ['ready', 'CV and search priorities ready?', true],
  ['add', 'You add documents or answer\nkey questions'],
  ['intake', 'ProfileIntake records verified facts\nand follows your document style'],
  ['search', 'JobFinder searches LinkedIn Jobs\nand employer sites; checks eligibility'],
  ['signin', 'If signed out, you sign in to LinkedIn\nthrough its official flow'],
  ['packet', 'Create a tailored CV, cover letter\nand application packet'],
  ['draft', 'Fill and check a portal draft\nwhen accessible'],
  ['outside', 'A checked application filled\noutside JobFinder'],
  ['profile', 'ProfileBuilder merges verified\nreusable answers into the private profile'],
  ['review', 'You review the application', true],
  ['selfsubmit', 'You submit the application'],
  ['finalize', 'ApplicationFinalize checks and submits\nonly with your direction'],
  ['confirm', 'EmailConfirmationChecker checks\nfor a matching receipt'],
  ['tracker', 'Tracker and packet record\nthe verified outcome'],
  ['followup', 'ApplicationFollowUp checks\nlater status when requested'],
];

const edges = [
  ['start', 'first'],
  ['first', 'setup', 'Yes'],
  ['first', 'check', 'No'],
  ['setup', 'check'],
  ['check', 'ready'],
  ['ready', 'add', 'No'],
  ['add', 'intake'],
  ['intake', 'check', '', 'constraint=false'],
  ['ready', 'search', 'Yes'],
  ['search', 'signin', 'Signed out', 'constraint=false'],
  ['signin', 'search', 'Resume', 'constraint=false'],
  ['search', 'packet'],
  ['packet', 'draft'],
  ['draft', 'profile'],
  ['outside', 'profile'],
  ['profile', 'review'],
  ['review', 'packet', 'Revisions', 'constraint=false'],
  ['review', 'selfsubmit', 'You submit'],
  ['review', 'finalize', 'Ask it to submit'],
  ['selfsubmit', 'confirm'],
  ['finalize', 'confirm'],
  ['confirm', 'tracker'],
  ['tracker', 'followup', 'Later update'],
  ['followup', 'tracker', '', 'constraint=false'],
  ['tracker', 'search', 'Next role reuses confirmed answers', 'constraint=false,style=dashed'],
];

function quoted(value) {
  return `"${value.replaceAll('\\', '\\\\').replaceAll('"', '\\"').replaceAll('\n', '\\n')}"`;
}

function source(rankdir, included = new Set(nodes.map(([id]) => id))) {
  const nodeLines = nodes.filter(([id]) => included.has(id)).map(([id, label, decision]) =>
    `  ${id} [label=${quoted(label)}${decision ? ',style="rounded,dashed,filled",fillcolor="#111111",color="#70b5f3"' : ''}];`
  );
  const edgeLines = edges.filter(([from, to]) => included.has(from) && included.has(to)).map(([from, to, label, extra]) =>
    `  ${from} -> ${to} [${[
      label ? `label=${quoted(label)}` : '', extra || '',
    ].filter(Boolean).join(',')}];`
  );
  return `digraph GetThatJob {
  graph [rankdir=${rankdir},bgcolor="#111111",pad=0.5,nodesep=0.45,ranksep=0.85,splines=polyline,outputorder=edgesfirst];
  node [shape=box,style="rounded,filled",fillcolor="#00182f",color="#355675",penwidth=2,fontname="Arial",fontsize=19,fontcolor="#d9e8f6",margin="0.22,0.18"];
  edge [color="#6f95b5",fontcolor="#70b5f3",fontname="Arial",fontsize=15,penwidth=2,arrowsize=0.8];
${nodeLines.join('\n')}
${edgeLines.join('\n')}
}`;
}

const viz = await instance();
const verticalDot = source('TB');
writeFileSync(join(here, 'workflow-detailed-vertical.dot'), verticalDot);
writeFileSync(join(here, 'workflow-detailed-vertical.svg'), viz.renderString(verticalDot, { format: 'svg' }));

const leftIds = new Set(['start', 'first', 'setup', 'check', 'ready', 'add', 'intake', 'search', 'signin']);
const rightIds = new Set(['packet', 'draft', 'outside', 'profile', 'review', 'selfsubmit', 'finalize', 'confirm', 'tracker', 'followup']);
const leftDot = source('TB', leftIds);
const rightDot = source('TB', rightIds);
writeFileSync(join(here, 'workflow-detailed-horizontal-left.dot'), leftDot);
writeFileSync(join(here, 'workflow-detailed-horizontal-right.dot'), rightDot);

function embedded(svg) {
  const match = svg.match(/<svg[^>]*viewBox="([^"]+)"[^>]*>([\s\S]*?)<\/svg>/);
  if (!match) throw new Error('Viz.js returned SVG without a viewBox');
  const [, viewBox, content] = match;
  const [, , width, height] = viewBox.split(/\s+/).map(Number);
  return { viewBox, content, width, height };
}

const left = embedded(viz.renderString(leftDot, { format: 'svg' }));
const right = embedded(viz.renderString(rightDot, { format: 'svg' }));
const margin = 80;
const gap = 260;
const header = 130;
const footer = 140;
const width = Math.ceil(margin * 2 + left.width + gap + right.width);
const height = Math.ceil(header + Math.max(left.height, right.height) + footer);
const leftY = header + (Math.max(left.height, right.height) - left.height) / 2;
const rightX = margin + left.width + gap;
const rightY = header + (Math.max(left.height, right.height) - right.height) / 2;
const arrowY = header + Math.max(left.height, right.height) / 2;
const horizontalSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
<rect width="100%" height="100%" fill="#111111"/>
<text x="${margin}" y="78" fill="#70b5f3" font-family="Arial" font-size="42" font-weight="bold">1. SET UP AND FIND</text>
<text x="${rightX}" y="78" fill="#70b5f3" font-family="Arial" font-size="42" font-weight="bold">2. PREPARE AND FOLLOW UP</text>
<svg x="${margin}" y="${leftY}" width="${left.width}" height="${left.height}" viewBox="${left.viewBox}">${left.content}</svg>
<svg x="${rightX}" y="${rightY}" width="${right.width}" height="${right.height}" viewBox="${right.viewBox}">${right.content}</svg>
<path d="M${margin + left.width + 45} ${arrowY} H${rightX - 45}" stroke="#70b5f3" stroke-width="8" fill="none" marker-end="url(#arrow)"/>
<defs><marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="16" markerHeight="16" orient="auto"><path d="M1 1 L11 6 L1 11" fill="none" stroke="#70b5f3" stroke-width="2"/></marker></defs>
<text x="${width / 2}" y="${height - 55}" text-anchor="middle" fill="#d9e8f6" font-family="Arial" font-size="30">Next role: reuse confirmed answers and recheck scoped facts before returning to JobFinder.</text>
</svg>`;
writeFileSync(join(here, 'workflow-detailed-horizontal.svg'), horizontalSvg);
console.log(join(here, 'workflow-detailed-horizontal.svg'));
console.log(join(here, 'workflow-detailed-vertical.svg'));
