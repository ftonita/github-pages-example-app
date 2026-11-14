import { cp, mkdir, rm, stat } from 'node:fs/promises';
import { resolve } from 'node:path';

const source = resolve(process.env.STATIC_SOURCE ?? 'public');
const output = resolve(process.env.STATIC_OUT ?? 'dist');

if (!(await stat(source).catch(() => null))?.isDirectory()) {
  throw new Error(`Каталог со статикой не найден: ${source}`);
}
if (source === output) {
  throw new Error('Исходный и выходной каталоги должны различаться');
}

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await cp(source, output, { recursive: true });
console.log(`Статика собрана: ${source} → ${output}`);
