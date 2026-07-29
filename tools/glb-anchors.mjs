/**
 * Report world-space anchor points from a built GLB, by node name.
 *
 * <model-viewer> hotspots are model-space coordinates, and the ones in the
 * content files were hand-converted from Blender. Blender is Z-up and glTF is
 * Y-up, so (bx, by, bz) becomes (bx, bz, -by) — the minus is easy to drop, and
 * dropping it mirrors every marker to the opposite face of the machine, where
 * it either floats in space or hides inside the body.
 *
 * This measures the shipped artefact instead of trusting the conversion: it
 * walks the node hierarchy, accumulates transforms, and prints the world-space
 * centre of the bounding box of every node whose name matches.
 *
 *   node tools/glb-anchors.mjs public/models/mf-2513-r8.v1.glb            # list
 *   node tools/glb-anchors.mjs public/models/mf-2513-r8.v1.glb Carriage Ink
 */
import { readFileSync } from 'node:fs';

const [file, ...patterns] = process.argv.slice(2);
if (!file) {
  console.error('usage: node tools/glb-anchors.mjs <file.glb> [namePattern...]');
  process.exit(2);
}

const buf = readFileSync(file);
if (buf.readUInt32LE(0) !== 0x46546c67) throw new Error(`${file} is not a GLB`);
const gltf = JSON.parse(buf.subarray(20, 20 + buf.readUInt32LE(12)).toString('utf8'));

const IDENTITY = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];

function multiply(a, b) {
  const out = new Array(16).fill(0);
  for (let i = 0; i < 4; i++)
    for (let j = 0; j < 4; j++)
      for (let k = 0; k < 4; k++) out[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k];
  return out;
}

function localMatrix(node) {
  if (node.matrix) return node.matrix.slice();
  const [tx, ty, tz] = node.translation ?? [0, 0, 0];
  const [x, y, z, w] = node.rotation ?? [0, 0, 0, 1];
  const [sx, sy, sz] = node.scale ?? [1, 1, 1];
  return [
    (1 - 2 * (y * y + z * z)) * sx, 2 * (x * y + z * w) * sx, 2 * (x * z - y * w) * sx, 0,
    2 * (x * y - z * w) * sy, (1 - 2 * (x * x + z * z)) * sy, 2 * (y * z + x * w) * sy, 0,
    2 * (x * z + y * w) * sz, 2 * (y * z - x * w) * sz, (1 - 2 * (x * x + y * y)) * sz, 0,
    tx, ty, tz, 1,
  ];
}

const apply = (m, p) => [
  m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
  m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
  m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14],
];

/** World-space bbox of a node's own meshes plus everything under it. */
function bbox(index, parent, into) {
  const node = gltf.nodes[index];
  const world = multiply(parent, localMatrix(node));
  if (node.mesh !== undefined) {
    for (const prim of gltf.meshes[node.mesh].primitives) {
      const acc = gltf.accessors[prim.attributes.POSITION];
      if (!acc?.min) continue;
      for (const cx of [acc.min[0], acc.max[0]])
        for (const cy of [acc.min[1], acc.max[1]])
          for (const cz of [acc.min[2], acc.max[2]]) {
            const w = apply(world, [cx, cy, cz]);
            for (let i = 0; i < 3; i++) {
              into.min[i] = Math.min(into.min[i], w[i]);
              into.max[i] = Math.max(into.max[i], w[i]);
            }
          }
    }
  }
  for (const child of node.children ?? []) bbox(child, world, into);
  return into;
}

const fresh = () => ({ min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] });
const fmt = (n) => (Math.abs(n) < 0.0005 ? '0' : n.toFixed(3).replace(/\.?0+$/, ''));

/** Parent index per node, so a match can be measured in world space. */
const parentOf = new Map();
gltf.nodes.forEach((n, i) => (n.children ?? []).forEach((c) => parentOf.set(c, i)));
function worldOf(index) {
  if (index === undefined) return IDENTITY;
  const chain = [];
  for (let i = index; i !== undefined; i = parentOf.get(i)) chain.unshift(i);
  let m = IDENTITY;
  for (const i of chain) m = multiply(m, localMatrix(gltf.nodes[i]));
  return m;
}

const whole = fresh();
for (const root of gltf.scenes[gltf.scene ?? 0].nodes) bbox(root, IDENTITY, whole);
console.log(
  `${file}\nbounds  x ${fmt(whole.min[0])}..${fmt(whole.max[0])}` +
  `  y ${fmt(whole.min[1])}..${fmt(whole.max[1])}` +
  `  z ${fmt(whole.min[2])}..${fmt(whole.max[2])}  (y is height)\n`,
);

const wanted = patterns.length ? patterns : null;
const seen = new Set();
gltf.nodes.forEach((node, i) => {
  const name = node.name ?? '';
  if (!name) return;
  if (wanted && !wanted.some((p) => name.toLowerCase().includes(p.toLowerCase()))) return;
  if (!wanted && seen.has(name.replace(/\d+$/, ''))) return;
  seen.add(name.replace(/\d+$/, ''));
  // Measured against the node's own place in the scene, parents included.
  const box = bbox(i, worldOf(parentOf.get(i)), fresh());
  if (!Number.isFinite(box.min[0])) return;
  const c = [0, 1, 2].map((k) => (box.min[k] + box.max[k]) / 2);
  const size = [0, 1, 2].map((k) => box.max[k] - box.min[k]);
  console.log(
    `${name.padEnd(24)} position="${fmt(c[0])} ${fmt(c[1])} ${fmt(c[2])}"` +
    `   size ${size.map(fmt).join(' × ')}`,
  );
});
