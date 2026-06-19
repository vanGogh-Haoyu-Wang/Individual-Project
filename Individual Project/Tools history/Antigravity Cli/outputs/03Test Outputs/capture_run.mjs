import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const [logPath, command, ...args] = process.argv.slice(2);
if (!logPath || !command) {
  throw new Error("Usage: node capture_run.mjs <log-path> <command> [args...]");
}

const started = new Date();
const result = spawnSync(command, args, {
  cwd: process.cwd(),
  env: process.env,
  encoding: "utf8",
  maxBuffer: 64 * 1024 * 1024,
});
const finished = new Date();
const status = result.status ?? 1;
const renderedCommand = [command, ...args].map((part) => JSON.stringify(part)).join(" ");
const log = [
  `STARTED: ${started.toISOString()}`,
  `FINISHED: ${finished.toISOString()}`,
  `CWD: ${process.cwd()}`,
  `COMMAND: ${renderedCommand}`,
  `EXIT_STATUS: ${status}`,
  "",
  "----- STDOUT -----",
  result.stdout ?? "",
  "----- STDERR -----",
  result.stderr ?? "",
  result.error ? `SPAWN_ERROR: ${result.error.stack ?? result.error}` : "",
].join("\n");

fs.mkdirSync(path.dirname(path.resolve(logPath)), { recursive: true });
fs.writeFileSync(logPath, log, "utf8");
process.stdout.write(log);
process.exitCode = status;
