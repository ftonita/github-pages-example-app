// Run with `node src/main.js` to generate a static site in dist/.
const fs = require('node:fs');
const path = require('node:path');

const outputDir = path.resolve(__dirname, '../dist');
fs.mkdirSync(outputDir, { recursive: true });

fs.writeFileSync(
	path.join(outputDir, 'index.html'),
	`<!doctype html>
<html lang="ru">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>GitHub Pages — пример</title>
	</head>
	<body>
		<main>
			<h1>Сайт опубликован!</h1>
			<p>Эта статическая страница собрана с помощью GitHub Actions.</p>
		</main>
	</body>
</html>
`,
	'utf8'
);

console.log('Static site generated in dist/');
