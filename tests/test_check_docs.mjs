import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { checkDocs } from "../scripts/check_docs.mjs";

const opts = { pythonExecutable: path.resolve(".venv/bin/python") };

async function fixture(t, readme, target = "# 概览\n\n# 概览\n") {
  const root = await mkdtemp(path.join(tmpdir(), "adk-doc-check-"));
  t.after(() => rm(root, { recursive: true, force: true }));
  await mkdir(path.join(root, "docs"));
  await writeFile(path.join(root, "README.md"), readme);
  await writeFile(path.join(root, "docs", "a b.md"), target);
  return root;
}

test("encoded paths and repeated Chinese headings resolve", async (t) => {
  const root = await fixture(t, "# 首页\n\n[目标](docs/a%20b.md#概览-1)\n");
  assert.deepEqual(await checkDocs(root, opts), []);
});

test("a missing anchor is reported at its source line", async (t) => {
  const root = await fixture(t, "# 首页\n\n[目标](docs/a%20b.md#不存在)\n");
  const problems = await checkDocs(root, opts);
  assert.equal(problems.length, 1);
  assert.equal(problems[0].path, "README.md");
  assert.equal(problems[0].line, 3);
  assert.match(problems[0].message, /anchor/i);
});

test("links inside fences are ignored", async (t) => {
  const root = await fixture(t, "# 首页\n\n~~~text\n[伪链接](missing.md)\n~~~\n");
  assert.deepEqual(await checkDocs(root, opts), []);
});

test("invalid Python is reported", async (t) => {
  const root = await fixture(t, "# 首页\n\n~~~python\ndef broken(\n~~~\n");
  const problems = await checkDocs(root, opts);
  assert.equal(problems.length, 1);
  assert.equal(problems[0].line, 4);
  assert.match(problems[0].message, /Python/);
});

test("missing local files and reference links are checked", async (t) => {
  const root = await fixture(t, "# Home\n\n[broken][ref]\n\n[ref]: absent.md\n");
  assert.equal((await checkDocs(root, opts)).length, 1);
});

test("valid Python is compiled but never executed", async (t) => {
  const root = await fixture(t, "# Home\n\n~~~python\nraise RuntimeError('must not run')\n~~~\n");
  assert.deepEqual(await checkDocs(root, opts), []);
});
