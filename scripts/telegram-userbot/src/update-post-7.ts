import "dotenv/config";
import { createClient } from "@supabase/supabase-js";

const NEW_CONTENT = `🌷 *Frühling heisst auch: Der Körper stellt sich um.*

Und wir Frauen spüren das oft besonders — Stimmungsschwankungen, Zyklus-Chaos, Hitzewallungen.

🌿 *Mein liebster Begleiter: der ClaryCalm Roll-On*

ClaryCalm ist ein fertiger Roll-On mit perfekt abgestimmter Frauen-Mischung. Aufmachen, anwenden, fertig. Kein Mischen, kein Verdünnen.

📍 *Anwendung:*
Vor allem in der zweiten Zyklushälfte auf Unterbauch, Handgelenk und Nacken.

🌿 *Wer gerne selber blendet:*

Roll-On (10ml):
• 4 Tropfen **Geranium**
• 3 Tropfen **Ylang Ylang**
• 2 Tropfen **Clary Sage**
• aufgefüllt mit Kokosöl

🌙 *Abend-Bonus:*
Bei Bedarf den **Balance Blend** auf die Fusssohlen — erdet wie kaum was anderes.

━━━━━━━━━━━━━━━━━━
Was sind deine hormonellen Frühlingsthemen? 💛

💛 *Hinweis:* Bei Schwangerschaft, Stillzeit oder Medikamenten bitte ärztlich abklären.`;

async function main() {
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  const { error } = await supabase
    .from("scheduled_posts")
    .update({ content: NEW_CONTENT })
    .eq("post_number", 7)
    .eq("status", "pending_approval");

  if (error) {
    console.error("❌", error);
    process.exit(1);
  }
  console.log("✅ Post 7 aktualisiert");
}

main();
