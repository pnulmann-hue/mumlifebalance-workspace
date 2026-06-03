---
tags: [doterra, oele, wissen, index]
---

# 🌿 doTERRA Öl-Wissensdatenbank

Volltext-extrahierte Öl-Wissensbibliothek von Patricia — durchsuchbar in **jeder** Claude-Session (Handy & PC), offline aus dem Repo.

## Was das ist & warum

Patricias komplette Öl-Bibliothek lebt als PDF in Google Drive (Ordner **„Öl-Wissen"**) und als Embeddings im Supabase-Brain des doTERRA-Bots (`doterra-bot.vercel.app`). **Claude Code** (dieses Repo) konnte da bisher nicht ran. Deshalb wurde hier der **Volltext** aller Öl-Dateien als Markdown abgelegt — leicht, schnell durchsuchbar (`grep`), auf jedem Gerät.

> ⚠️ **Hinweis zur Qualität:** Der Text wurde automatisch aus PDFs extrahiert. Bei gescannten Büchern (Schasteen u.a.) kann OCR-Rauschen oder unvollständiger Text auftreten. Die **Original-PDFs in Google Drive** bleiben die maßgebliche Quelle. Jede Datei verlinkt ihr Original.

## So suchst du

```bash
# Welches Öl gegen X?
grep -rli "schweiss\|geruch\|deo" reference/doterra-oele/
grep -rli "haare\|kopfhaut\|haarwuchs" reference/doterra-oele/
# Volltext einer Datei lesen → einfach öffnen
```

## Struktur

| Ordner | Inhalt |
|---|---|
| `buecher/` | Große Aromatherapie- & Network-Bücher (mehrkapitelig) |
| `enjoils/<saison>/` | doTERRA Enjoils-Magazine — Einzelöl-Sheets + Themen, saisonal |
| `referenz/` | Sicherheit, Verdünnung, Wirkstoff-Chemie, Methodik |
| `oel-wissen/` | Übrige Themenhefte aus dem Hauptordner |

## Quelle: Google Drive

- **Hauptordner „Öl-Wissen":** https://drive.google.com/drive/folders/1TuKVEpJK20aV1AuKuQSH10tbXMD7hZ68
- **Enjoils:** https://drive.google.com/drive/folders/1kTt3QWwV9IlIfPcEXRAyxSg9QTEZKj2A

---

## 📋 Inventar (Drive-IDs)

### buecher/
- Duftmedizin – Das Praxisbuch · Maria L. Schasteen — `1oKR4YujWKy9piG5ZpOdAMdoO9QxfrQPI`
- Duftmedizin mit Zitrone · Maria L. Schasteen — `1pnvTuCezt9m5fiZkTocmINPJtACXwavx`
- Erkältung · Maria L. Schasteen — `1aZZ0k_9_d2VEsuiWIKh2sadWspwKCNmy`
- Duft Medizin für Kinder · Maria L. Schasteen — `1GdcErlvoZ5X2amqRdKFWU8VH02sgL07s`
- Schlafstörungen / Besser schlafen · Schasteen — `17w0g4E_1xJpHUaCOuY9ZkuVbT7oCr8_0`
- Praxis-Aromatherapie · Werner — `1puoy39AkDSfC1O-b3VyspNBnd6ZbWv1k`
- Holistische Aromatherapie · Mock/Hanika — `1gVhGdd0e8g5HiedfBo0vNw_hYlRk6f_d`
- Öle, die die Seele heilen · Felicity Warner — `1B8ET78pLqNTAdi0rwDuUHFuVCp5u9L3r`
- Aromatherapie für Kinder · Herber — `1UOyKTs9tlQxrPIhW2e8334_ot3j4I-Zm`
- Kinder sanft & natürlich heilen · Jahn — `1rPyYsufES5uIoQyf7Qbyy94IV-HjT7Vd`
- GoPro · Eric Worre — `15w1P9u3oKQ4pt_eYM3kDNijNpf6O4LsJ`
- Unbox your Network — `1tBBCyPkx-uw0CjowYhnQ2JuFyU8TW26F`
- Spiritual Leadership · Mahlow — `1sFpoh-osYh6BJuAwxm2iW5gTVUMX0vRu`
- doTERRA Lead Guide — `1aKXGr51FEjqBQYhvhN3pBjb-eejBiBi1`

### referenz/
- Leitfaden zur sicheren Anwendung ätherischer Öle — `1oabtAN9z9e9nw5lEfozOk_5eamfI6Ii6`
- Wirkstoffwissen – Oxide — `1oiBoeVQsBfpOtV-Bm0njJi_xn5TCKx-n`

### oel-wissen/ (Hauptordner-Themen)
- Patricia Wendepunkt-Story — `10-HREnLnuBJAgqff1rtO_ttno3WzWRbP`
- Zimt (OCR) — `1xJ00ZUP1OhHo_tphwF-kCt4xxYTxSboN`
- Myrrhe (OCR) — `1MvB5h46-lzPbglZKz856HIGKl4m0YcS-`
- Thymian (OCR) — `1wD2VoCHsXkUZrzjrBi0SLQJMsh5YBbtv`
- Enjoils Winter 2024 (OCR) — `1TSdYqnBj4iE0iGhcje4bq1p-Lj_ybEir`
- Gesund im Winter (OCR) — `1iVOKlHCaED5YanXvO64N-x08Pl7F2Xit`
- Ätherische Öle & Sauna — `1f-qx4tyz1q9DEVKBv06fjHkvXOQGtg2U`
- Suppen & Eintopf mit ätherischen Ölen — `1dFjzIK1CEB0GaM-8ZNMZ4WNobcQdfDcd`
- Winterzeit, Feiertage, Rauhnächte — `1q4L9645Qm4AQ1DI4iLJlh7vpckWHdiRJ`
- Schlaf gut — `115r1uQFuAxXcM4h7BXW4frzqg-bY0UMg`
- Innehalten — `1KM1tbf3TI97SFvZZ6ML8rNMRgIyoIMiY`
- Selbstliebe Duftmischung — `18xpugtJ4bJUNSECndemkOMJ3CXsn-MgZ`
- Solfeggio — `1MqZY1kg8qX0iBZnkmUHvQlA-aZ7YHTuB`

### enjoils/fruehling-2024/
Selbstliebe & Ermächtigung `15cocLK78Aji0D3hccuV7XcRtVHZthaJv` · Aromatisch durch den Frühling `1Zt21g_vrnMz-TInRPv41eJFuglw-W4Af` · Schilddrüse `1-Xs5f7MjeDTCAmCChKIWZnzW2yEaCvr7` · Heilkraft fürs Hirn `1HK9yFyH971wKQoUr9zUXLlMrH68889oL` · Zitrone `1tZdEwpj2it4WGem2xlMkSay9qrjrL64N` · Ester `1_Ng2uKAiz4XlOSsm2GqQE6cfw-Hwa1SX` · Rose `1YOqSgE-LbAB-Y-bQ8JFwXrzclvxK7CEt` · Ballast loswerden `1bkVmUTVpKVpfkWly8p_iflewRy2ZbkJF` · Arborvitae `1KudcmoVVD733x7njYNl8rOANyF_yNJs9` · Diffusermischungen `12FVxrBiHzBKJJ4xiYuUwajgxhK4pwfEz`

### enjoils/sommer-2024/
Duftmedizin für Kinder `1mbsBw_-XZzQlACmbraQza3EG8Za_nQep` · Schutz vor Insekten `1XLScgrXOckBhqvJpaJ_ZybZr5H_1wqVZ` · Mitochondrien `1R16k9hS4gqYw6FCRESu0GUnrTL49Ov7c` · Natürliche Reinigung `1EKZzxHzI5mIIwzCeeQ-40roCnugVDI1-` · Cumarin `1ls5WQwbxnVot7DOqX7w09ZyREaLb0ZFJ` · Schmerzen natürlich lindern `1rDJlfcOsEJqiFWhuwTyFSEcCfA-7t5-d` · Grapefruit `1PE6DdtjZnFZoEft1hYy7OH69Ot2pS2Dp` · Geranium `1-PXoEFPNPeyarf47YWpSlamYwucnpU8L` · Basilikum `1-K18j893LvqzO0hQLIKOFSaGtustiRTf` · Aromatisch durch den Sommer `1SqW8EPw89hVsLjeIBLFrtA2HOrsvCfPt` · Diffusermischungen `1pFD6fgQfrqAKMADiQsiAbmHQtW3PuPNW`

### enjoils/herbst-2024/
Ingwer (Zusammenführen) `1g841EoXNeGMAXJa-Vbk1ALz5tL1ru4du` · Herbst `1c-jgIw2nQEemQY5LPpsJqRX09lMSSbJd` · Sesquiterpene `1pKkBmwyMgt5cRYBd1e1WzDgCQmWZu4Wa` · Leber `1hJWg67hAx231Eebk821MPPvnTeKtUKCO` · Herbstliche Aromaküche `1wbo0ek-AO_mHU5QFzh7WKBDufTxra9c6` · Oregano `18xoPFoL9VXvTbe6l2R5xuHREDHltXFju` · Kamille `1TPxhIw8aZGewfMlJK8HJAwRFTx-cuTo-` · Ingwer `1DVu0Pgchv7PnD0IMaMX4DCDydwXaYmd-` · In Liebe Roll-on `1ZcCfWSQj_u1jNOzUQ99Ox4kA9aTXvDaq` · Ich-Bin Roll-on `1nz9A0IcbYeM4Auz0jP3SVLQ0fmo2p7Kt` · Herbstzauber Duftmischung `1Niz-Lji1PPLYXMIAe4HnUF_2e50a25qR` · DIY `12Zp3m-vbAEWe9RSvuxLXmzwNeED_nLwY`

### enjoils/fruehling-2025/
Wirkung ätherischer Öle `1L-AEff5gTNYKCYM1kvaNV_pSotE7aTu5` · Ölziehen `1gFqPSM7D5CuMRGg5SQWcwalGdlSz1lV3` · Teebaumöl `1o54LbFQjh9SDUP2WGEPUdwKU3DCKf3Sl` · Stoffwechsel `1YDP9jGm-LbR--PgqLmK_RNh1Ogo9rnh-` · Magnolie `1DliL5-TaMF3sN11ti8oJ318FNrVkHUsD` · Frühlingsdiffuser `1-ZXZdcJCzdEg3iVw4FQYyPlFw78SsjSQ` · Organuhr `1nAScJBpzoWh_Yp3u4b8Q6jRqp1ZnTlFb` · Die Macht der Worte `1wBn7bJF6o_IhD9rNN6imlmufmFHYn5r1` · Frühling für Körper, Geist, zu Hause `1IHfMiG96jAxbrqwJu88hy1viZKbO2WDX` · Kurkuma `1gAcJoJVo5zztSdoqsJhDi7ObMosjWXR9` · Pollenflug & Allergien `1r_gSFs1SSILswJmry2IEtPtsv4VviNQs` · Abnehmstrategien `1IIcb6BhHMFftVHI6wSwFhwrABWvyV27o`

### enjoils/sommer-2025/
Reflexzonen & Aromatherapie `1PL9TjYg86BkhfU9Szi6nxhoewTNdq1Op` · Destillationsmethoden `1IPidJD9uklULphSsNgEtnhE7H-iwgt5Q` · Rosmarin `1R45BkxTpJU8EPOnV9AwWJv1U4mRU63EI` · Fermentation `12VZxvZ20g37x-O1msWBgC4CuyDUUfz3G` · Nervensystem `17iDpN326V2TxuuqzhDNOZ1CfIaPpW7yF` · Jasmin `17Edy87eNZKrcwJOoM4jNzk5NoHO-H52T` · Duftanker & Erinnerung `1Ny4zXCPWKLky9Dsh3YpZewLc8Ib8LjvS` · Öle und Sommer `1zSGawviD2VnGKOiKXwz5de9BHR2s8CZJ` · Reiseübelkeit `1xcdB9QzXuQKr1b94c00XyZhySlX4zPly` · Mandarine `1ZfwOPwyfJNjR6c4w7dGsvZsdqXMunZ44` · Diffuser- und Rollerrezepte `1bt7QPz5h6-gVCs4cbp8IRSU2vPM3CtLx`
