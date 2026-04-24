/**
 * Importiert 32 direkte doTERRA-Kunden in ActiveCampaign:
 * - Kontakt erstellen/aktualisieren (contact/sync ist idempotent)
 * - Liste 20 "doTERRA Kunden" zuweisen
 * - Tag 56 "doterra-kunde" + Mitgliedsart-Tag
 *
 * Ausgeschlossen: 3 Ghost Legs + 4 DSGVO-inforemoval
 */

const AC_URL = "https://mumlifebalance.api-us1.com";
const AC_KEY = "b3c3542991489fc766fe5f8e0f570412769b252ea525f75a33d72a8944e0fba5b0bf4e29";
const LIST_ID = 20;
const TAG_ALL = 56; // doterra-kunde
const TAG_VK = 57;  // doterra-vorteilskunde
const TAG_WA = 58;  // doterra-wellness-advocate

// 32 direkte Kunden (ohne Ghost Legs + ohne DSGVO-removals)
const customers = [
  { name: "Miriam Gätzi-Widmer",     email: "miriam_widmer@hotmail.com",       phone: "004-179-356-2660", type: "WA", doterraId: "14345977" },
  { name: "Corinne Heimgartner",     email: "corinne.messmer@hotmail.com",     phone: "079-270-3981",     type: "WA", doterraId: "14394698" },
  { name: "Edith Zuberbühler",       email: "edith.z@hotmail.ch",              phone: "",                 type: "VK", doterraId: "14675544" },
  { name: "Mirella Castellazzi",     email: "m.castellazzi98@gmail.com",       phone: "078-797-9807",     type: "WA", doterraId: "15123605" },
  { name: "Sonja Gülünay",           email: "sonja_gueluenay@hotmail.com",     phone: "076-580-3201",     type: "VK", doterraId: "15137945" },
  { name: "Olivia Sutter",           email: "olivia_rechsteiner@msn.com",      phone: "079-175-3439",     type: "VK", doterraId: "15403484" },
  { name: "Corinne Matter",          email: "corinne_matter@outlook.com",      phone: "079-539-6577",     type: "VK", doterraId: "15404565" },
  { name: "Michelle Berger",         email: "mj.berger90@gmail.com",           phone: "004-176-390-5257", type: "WA", doterraId: "15552586" },
  { name: "Claudia Schweizer",       email: "schweizerclaudia@gmail.com",      phone: "077-400-6088",     type: "VK", doterraId: "15595708" },
  { name: "Corina Rusch",            email: "corinarusch@hotmail.com",         phone: "076-576-2003",     type: "VK", doterraId: "16004071" },
  { name: "Manuela Streule",         email: "manuela_signer@hotmail.com",      phone: "078-622-9133",     type: "WA", doterraId: "16622339" },
  { name: "Claudia Höhener",         email: "hoehener.claudia@gmail.com",      phone: "079-719-3872",     type: "VK", doterraId: "16768290" },
  { name: "Nadine Steingruber",      email: "n.steingruber14@gmail.com",       phone: "079-103-5422",     type: "WA", doterraId: "16934110" },
  { name: "Melanie Kunz",            email: "Kunz.renato.84@gmail.com",        phone: "078-773-9153",     type: "WA", doterraId: "16982542" },
  { name: "Martina Meier",           email: "Ursundmartina@bluewin.ch",        phone: "004-178-833-0340", type: "VK", doterraId: "16988251" },
  { name: "Angela Inauen",           email: "angela.inauen@hotmail.com",       phone: "079-769-2219",     type: "VK", doterraId: "17451024" },
  { name: "Petra Neff",              email: "petrainauen85@gmx.ch",            phone: "078-859-1199",     type: "VK", doterraId: "17524790" },
  { name: "Silvia Moser",            email: "Silvia.buerki@gmx.ch",            phone: "079-363-4990",     type: "WA", doterraId: "17527961" },
  { name: "Verena Zellweger",        email: "v.zellweger89@gmail.com",         phone: "079-457-2409",     type: "VK", doterraId: "17532192" },
  { name: "Maria Rusch",             email: "Rmrusch@hispeed.ch",              phone: "004-178-870-4326", type: "VK", doterraId: "17564699" },
  { name: "Keerthiha Ulmer",         email: "keerthiha.s_95@hotmail.com",      phone: "004-178-645-0394", type: "VK", doterraId: "17565486" },
  { name: "Janine Manser",           email: "Fuster.janine@gmail.com",         phone: "078-888-5328",     type: "VK", doterraId: "17584356" },
  { name: "Wiebke Stein",            email: "wiebke.stein@bluewin.ch",         phone: "",                 type: "VK", doterraId: "17595619" },
  { name: "Anna Muff",               email: "anna.muff99@gmail.com",           phone: "076-710-2533",     type: "VK", doterraId: "17670977" },
  { name: "Ursula Manser",           email: "ursula.ulmann@gmail.com",         phone: "078-841-3619",     type: "VK", doterraId: "17891034" },
  { name: "Philipp Hongler",         email: "philipp.hongler@hotmail.com",     phone: "417-649-0675",     type: "VK", doterraId: "18004363" },
  { name: "Jasmine Walser",          email: "jasmine.weber@bluewin.ch",        phone: "079-714-2889",     type: "VK", doterraId: "18102159" },
  { name: "Andrea Inauen",           email: "inauen-graf@bluewin.ch",          phone: "078-642-3029",     type: "VK", doterraId: "18102166" },
  { name: "Monika Müller Kuster",    email: "Info@mumlifebalance.ch",          phone: "079-176-1407",     type: "VK", doterraId: "18144446" },
  { name: "Martina Burkhalter",      email: "m-burkhalter@hotmail.com",        phone: "079-613-9299",     type: "VK", doterraId: "18188491" },
  { name: "Lucrezia Burkard",        email: "lucrezia.burkard@gmail.com",      phone: "077-252-7512",     type: "VK", doterraId: "18644286" },
  { name: "Isabelle Röllin",         email: "isabelle.roellin@bluewin.ch",     phone: "079-448-7939",     type: "VK", doterraId: "18757359" },
];

async function ac(method, path, body) {
  const res = await fetch(`${AC_URL}/api/3/${path}`, {
    method,
    headers: { "Api-Token": AC_KEY, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`AC ${res.status}: ${JSON.stringify(data).slice(0, 200)}`);
  return data;
}

async function importCustomer(c) {
  // Name aufteilen
  const parts = c.name.trim().split(/\s+/);
  const firstName = parts[0];
  const lastName = parts.slice(1).join(" ");

  // 1. Contact sync (idempotent: create or update)
  const syncRes = await ac("POST", "contact/sync", {
    contact: {
      email: c.email,
      firstName,
      lastName,
      phone: c.phone || undefined,
      fieldValues: [], // Custom fields later
    },
  });
  const contactId = syncRes.contact.id;

  // 2. Liste 20 zuweisen (status 1 = subscribed)
  try {
    await ac("POST", "contactLists", {
      contactList: { list: LIST_ID, contact: contactId, status: 1 },
    });
  } catch (e) {
    // falls schon in Liste: ignorieren
    if (!String(e.message).includes("already")) console.warn(`  ⚠ List: ${e.message.slice(0,80)}`);
  }

  // 3. Tags
  const tagsToAdd = [TAG_ALL, c.type === "WA" ? TAG_WA : TAG_VK];
  for (const tagId of tagsToAdd) {
    try {
      await ac("POST", "contactTags", {
        contactTag: { contact: contactId, tag: tagId },
      });
    } catch (e) {
      // schon getaggt: ignorieren
    }
  }

  return contactId;
}

async function main() {
  console.log(`📥 Importiere ${customers.length} doTERRA-Kunden in AC Liste ${LIST_ID}...`);
  let ok = 0, fail = 0;
  for (const c of customers) {
    try {
      const id = await importCustomer(c);
      console.log(`  ✅ ${c.name.padEnd(32)} → AC-ID ${id} (${c.type})`);
      ok++;
    } catch (e) {
      console.error(`  ❌ ${c.name}: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n🎉 Fertig: ${ok} importiert, ${fail} Fehler`);
}

main();
