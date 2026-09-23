import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const baseUrl = process.env.APP_URL || "http://127.0.0.1:8511";
const docsDir = path.dirname(fileURLToPath(import.meta.url));
const screenshotRoot = path.join(docsDir, "assets", "screenshots");

const pages = [
  { locale: "en", name: "home", route: "/" },
  { locale: "ja", name: "home", route: "/home_(Japanese)" },
  { locale: "en", name: "simple", route: "/4D_Earthquake_Simple" },
  { locale: "ja", name: "simple", route: "/4D_Earthquake_%E3%82%B7%E3%83%B3%E3%83%95%E3%82%9A%E3%83%AB%E7%89%88" },
  { locale: "en", name: "advanced", route: "/4D_Earthquake_Advanced" },
  { locale: "ja", name: "advanced", route: "/4D_Earthquake_%E8%A9%B3%E7%B4%B0%E7%89%88" },
];

  await mkdir(path.join(screenshotRoot, locale), { recursive: true });
}

const launchOptions = { headless: true };
if (process.env.CHROME_PATH) {
  launchOptions.executablePath = process.env.CHROME_PATH;
}
const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({
  viewport: { width: 1440, height: 1000 },
  deviceScaleFactor: 1,
});

for (const target of pages) {
  await page.goto(`${baseUrl}${target.route}`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector("[data-testid='stAppViewContainer']", { timeout: 30000 });
  await page.waitForTimeout(target.name === "home" ? 2500 : 10000);

  const output = path.join(screenshotRoot, target.locale, `${target.name}.png`);
  await page.screenshot({ path: output, fullPage: false });

  if (target.name === "advanced") {
    const comparisonTab = target.locale === "ja" ? "🧪 比較" : "🧪 Comparison";
    const dataTab = target.locale === "ja" ? "🗂️ データ（CSV）" : "🗂️ Data(CSV)";

    await page.getByRole("tab", { name: comparisonTab }).click();
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotRoot, target.locale, "advanced-comparison.png"),
      fullPage: false,
    });

    await page.getByRole("tab", { name: dataTab }).click();
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotRoot, target.locale, "advanced-data.png"),
      fullPage: false,
    });
  }

  const headings = await page.locator("h1, h2, h3").allTextContents();
  console.log(`${target.locale}/${target.name}: ${headings.slice(0, 8).join(" | ")}`);
}

await browser.close();
