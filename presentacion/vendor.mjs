import { cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// Copy prebuilt engine files; this does not compile Reveal.js.
const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, 'node_modules', 'reveal.js');
const installed = JSON.parse(await readFile(join(source, 'package.json'), 'utf8'));
const project = JSON.parse(await readFile(join(root, 'package.json'), 'utf8'));
if (installed.version !== project.dependencies['reveal.js']) {
  throw new Error('Installed Reveal.js differs from the exact package.json pin. Run npm install.');
}
const target = join(root, 'assets', 'vendor', 'reveal');
await mkdir(target, { recursive: true });
await cp(join(source, 'dist'), target, { recursive: true });
await cp(join(source, 'LICENSE'), join(target, 'LICENSE'));
await writeFile(join(target, 'version.json'), JSON.stringify({ version: installed.version }) + '\n');
console.log(`Reveal.js ${installed.version} local en assets/vendor/.`);

const katex = join(root, 'node_modules', 'katex');
const mathPackage = JSON.parse(await readFile(join(katex, 'package.json'), 'utf8'));
if (mathPackage.version !== project.dependencies.katex) {
  throw new Error('La versión instalada de KaTeX difiere de package.json.');
}
const math = join(root, 'assets', 'vendor', 'katex');
await mkdir(math, { recursive: true });
for (const name of ['katex.min.js', 'katex.min.css', 'fonts']) {
  await cp(join(katex, 'dist', name), join(math, name), { recursive: true });
}
await cp(join(katex, 'LICENSE'), join(math, 'LICENSE'));
console.log(`KaTeX ${mathPackage.version} local en assets/vendor/.`);
