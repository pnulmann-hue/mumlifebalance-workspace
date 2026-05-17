/**
 * Sweep über alle 3 Mailboxen (GMX, Hoststar, Gmail).
 * Run: npx tsx src/run-mail-sweep-all.ts
 */

import * as dotenv from "dotenv";
dotenv.config({ override: true });

import { runMailSweep } from "./mail-poller";

const userId = parseInt(process.env.PATRICIA_TELEGRAM_USER_ID || "0");

runMailSweep(userId).then(() => {
  console.log("✅ Alles fertig.");
  process.exit(0);
}).catch((err) => {
  console.error("❌", err);
  process.exit(1);
});
