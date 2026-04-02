import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import MarkdownIt from "markdown-it";
import GithubSlugger from "github-slugger";

const markdown = new MarkdownIt({ html: true });
const excluded = new Set(["node_modules", ".validation", ".venv", ".venv-310", ".git"]);

export async function documentFiles(root) {
  const files = [];
  async function walk(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (excluded.has(entry.name)) continue;
      const target = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(target);
      else if (entry.isFile() && entry.name.endsWith(".md")) files.push(target);
    }
  }
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const target = path.join(root, entry.name);
    if (entry.isFile() && entry.name.endsWith(".md")) files.push(target);
    if (entry.isDirectory() && ["docs", "examples", ".github"].includes(entry.name)) await walk(target);
  }
  return files.sort();
}

function headingText(tokens) {
  return tokens.map((token) => {
    if (["text", "code_inline", "image"].includes(token.type)) return token.content;
    if (["softbreak", "hardbreak"].includes(token.type)) return " ";
    return token.children ? headingText(token.children) : "";
  }).join("");
}

/** Check local Markdown links and compile Python fences without executing them. */
export async function checkDocs(root, { pythonExecutable }) {
  root = path.resolve(root);
  const problems = [];
  const parsed = new Map();
  async function parse(file) {
    if (!parsed.has(file)) {
      const tokens = markdown.parse(await readFile(file, "utf8"), {});
      const slugger = new GithubSlugger();
      const anchors = new Set();
      for (let i = 0; i < tokens.length; i += 1) {
        if (tokens[i].type === "heading_open") {
          anchors.add(slugger.slug(headingText(tokens[i + 1].children || [])));
        }
      }
      parsed.set(file, { tokens, anchors });
    }
    return parsed.get(file);
  }
  for (const file of await documentFiles(root)) {
    const relative = path.relative(root, file);
    const { tokens } = await parse(file);
    const problem = (line, message) => problems.push({ path: relative, line, message });
    for (const token of tokens) {
      if (token.type === "fence" && ["python", "py", "python3"].includes(token.info.split(/\s+/)[0])) {
        const result = spawnSync(pythonExecutable, [
          "-c", "import sys; compile(sys.stdin.read(), sys.argv[1], 'exec')", relative,
        ], { input: token.content, encoding: "utf8", timeout: 10000 });
        if (result.error || result.status !== 0) {
          const output = result.stderr || String(result.error || "compiler failed");
          const offset = Number(output.match(/line (\d+)/)?.[1] || 1);
          problem((token.map?.[0] || 0) + 1 + offset,
            "Python: " + output.trim().split("\n").at(-1));
        }
      }
      if (token.type !== "inline") continue;
      for (const child of token.children || []) {
        const href = child.type === "link_open" ? child.attrGet("href")
          : child.type === "image" ? child.attrGet("src") : null;
        if (href === null || /^[a-z][a-z\d+.-]*:/i.test(href) || href.startsWith("//")) continue;
        const line = (token.map?.[0] || 0) + 1;
        let localPath, fragment;
        try {
          const hash = href.indexOf("#");
          localPath = decodeURIComponent((hash < 0 ? href : href.slice(0, hash)).split("?")[0]);
          fragment = hash < 0 ? "" : decodeURIComponent(href.slice(hash + 1));
        } catch {
          problem(line, "Invalid URL encoding: " + href);
          continue;
        }
        const target = localPath ? path.resolve(path.dirname(file), localPath) : file;
        const fromRoot = path.relative(root, target);
        if (fromRoot === ".." || fromRoot.startsWith(".." + path.sep) || path.isAbsolute(fromRoot)) {
          problem(line, "Local link leaves repository: " + href);
          continue;
        }
        let info;
        try {
          info = await stat(target);
        } catch (error) {
          if (!["ENOENT", "ENOTDIR"].includes(error.code)) throw error;
          problem(line, "Missing local file: " + href);
          continue;
        }
        if (fragment && info.isFile() && target.endsWith(".md") && !(await parse(target)).anchors.has(fragment)) {
          problem(line, "Missing anchor: " + href);
        }
      }
    }
  }
  return problems;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const pythonIndex = process.argv.indexOf("--python");
  const pythonExecutable = pythonIndex >= 0 ? process.argv[pythonIndex + 1] : ".venv/bin/python";
  try {
    const problems = await checkDocs(process.cwd(), { pythonExecutable });
    for (const p of problems) console.error(p.path + ":" + p.line + ": " + p.message);
    if (problems.length) process.exitCode = 1;
    else console.log((await documentFiles(process.cwd())).length + " Markdown files: links and Python fences valid");
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
