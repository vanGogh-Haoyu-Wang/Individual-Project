import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath = process.argv[2];
const outputPath = process.argv[3];

if (!workbookPath || !outputPath) {
  throw new Error("Usage: node inspect_workbook.mjs <workbook.xlsx> <output.txt>");
}

const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const summary = await workbook.inspect({
  kind: "workbook,sheet,table",
  include: "id,name,values,formulas",
  maxChars: 20000,
  tableMaxRows: 12,
  tableMaxCols: 16,
  tableMaxCellChars: 100,
});

const text = [
  `Workbook: ${path.resolve(workbookPath)}`,
  `Inspected: ${new Date().toISOString()}`,
  "",
  summary.ndjson,
  "",
].join("\n");

await fs.writeFile(outputPath, text, "utf8");
process.stdout.write(text);
