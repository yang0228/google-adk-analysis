import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import MarkdownIt from "markdown-it";
import { documentFiles } from "./check_docs.mjs";

const root = process.cwd();
const output = path.join(root, ".validation", "diagrams");
await mkdir(output, { recursive: true });
const config = path.join(output, "mermaid.json");
await writeFile(config, JSON.stringify({
  theme: "neutral",
  themeVariables: { fontFamily: "Noto Sans CJK SC, PingFang SC, sans-serif" },
  flowchart: { htmlLabels: false, useMaxWidth: true },
}));
const browserConfig = path.join(output, "puppeteer.json");
// Linux CI can restrict Chromium user-namespace sandboxing.
// The renderer only consumes repository-controlled Mermaid, never remote pages.
await writeFile(browserConfig, JSON.stringify(
  process.platform === "linux" ? { args: ["--no-sandbox"] } : {},
));
let count = 0;
const parser = new MarkdownIt();
for (const file of await documentFiles(root)) {
  let number = 0;
  for (const token of parser.parse(await readFile(file, "utf8"), {})) {
    if (token.type !== "fence" || token.info.trim() !== "mermaid") continue;
    number += 1;
    count += 1;
    const name = path.relative(root, file).replace(/\.md$/, "").replaceAll(path.sep, "--") + "-" + number;
    const input = path.join(output, name + ".mmd");
    await writeFile(input, token.content);
    for (const format of process.argv.includes("--png") ? ["svg", "png"] : ["svg"]) {
      const result = spawnSync(process.execPath, [
        path.join(root, "node_modules/@mermaid-js/mermaid-cli/src/cli.js"),
        "-i", input, "-o", path.join(output, name + "." + format),
        "-c", config, "-p", browserConfig, "-b", "white", "--size", "1600",
      ], { encoding: "utf8", timeout: 60000 });
      if (result.error || result.status !== 0) {
        console.error(path.relative(root, file) + ":" + ((token.map?.[0] || 0) + 1) + ": Mermaid render failed");
        console.error(result.stderr || result.error);
        process.exit(1);
      }
    }
  }
}
if (!count) {
  console.error("No Mermaid diagrams found");
  process.exitCode = 1;
} else console.log(count + " Mermaid diagrams rendered to .validation/diagrams");
