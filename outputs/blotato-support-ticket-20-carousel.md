# Blotato Support Ticket — Request: Support Instagram's New 20-Slide Carousel Limit

**Zum Einreichen:** Blotato Support Chat / E-Mail an Support

---

## Subject

API Feature Request: Support Instagram's expanded 20-image carousel limit

---

## Body

Hi Blotato Team,

I'd like to request support for Instagram's expanded carousel limit of 20 images per post. Currently the Blotato API rejects carousel posts with more than 10 images.

**What happened:**
I scheduled an Instagram carousel post with 11 images via the Blotato API (`POST /v2/posts`) for my account `@mumlifebalance_patricia_ulmann` (Blotato accountId `41414`). The submission returned `201 Created` with a valid `postSubmissionId`, but the post failed at publishing time with:

```
Status: failed
Error: "Could not publish on Instagram: Unsupported post type.
        The post has too little or too many attachments to qualify as a carousel"
```

I re-submitted the same post with only 10 images and it published successfully, which confirms the 10-image cap is the blocker.

**The Instagram change:**
Instagram expanded the carousel limit from 10 to 20 images in 2024/2025. My account has this feature active — I can manually post 11-20 image carousels through the Instagram mobile app without any issue.

**What I'd love:**
Could you update the Blotato API validation to allow up to 20 `mediaUrls` for Instagram carousel posts? My understanding is Instagram's Graph API already supports this (up to 20 children in a CAROUSEL media container), so it may only require relaxing the Blotato-side validation.

**My use case:**
I post educational carousels for a mom-focused mentoring audience. Longer carousels (12-18 slides) perform significantly better for my topics (saves + shares) than forcing the content into 10 slides. Right now I either have to cut content or post manually, which breaks my automation.

**Request summary:**
- Raise the `mediaUrls` max for Instagram carousels from 10 → 20
- Alternatively: expose a config flag so accounts with the 20-image feature enabled can opt in

Happy to test anything once it's available.

Thanks for a great tool,
Patricia Ulmann
`@mumlifebalance_patricia_ulmann` (accountId 41414)
`@patricia_ulmann` (accountId 41413)

---

## Ablauf zum Einreichen

1. Einloggen auf [blotato.com](https://blotato.com)
2. Support-Chat rechts unten oder E-Mail an `support@blotato.com`
3. Obigen Body einfügen (inkl. Subject)
4. Absenden

## Was wir als Antwort hoffen

- Bestätigung dass sie's aufnehmen (1-8 Wochen Rollout typisch)
- Oder Confirmation dass Instagram Graph API das bei ihnen auch noch nicht unterstützt

## Was ich fürs Interim baue

Im `/montag`-Workflow bleibt Karussell-Folien-Anzahl **default max 10** für Blotato-Posts, bis Blotato 20 supportet. Dann flipp ich die Memory-Regel um.
