# Prompt for Antigravity: independent Bhumi product review

Read AGENT_LOG.md first. Codex has added Entry 015 and a product review at docs/bhumi_product_truth_audit_and_10_year_approach.md. This is a shared-workspace handoff: inspect the live app and current source independently, then reply in the shared log. Do not assume the claims in either the UI or the log are true without checking them.

The user wants Bhumi to become a farmer-first product for Hosanagalapura/Molakalmuru, with no hardcoded crop choices or farm facts, crop recommendations based on relevant weather and market evidence, locally important seeds such as Dolly field bean and Naavi/Navi ridge gourd represented correctly, real mandi prices, useful motion graphics, and a credible long-term approach.

Please do a brief read-only verification first. Do not stop/restart or overwrite the shared server. After logging findings in Entry 016, immediately start the frontend fixes you already own in frontend/farmer_app.html: remove the fabricated parcel polygon and authentication claims; hide unsupported soil, acreage, profit, and market values; correct Sentinel-2/NDVI labels; fix repeated yield sublabels and static voice output; and make language coverage and missing-data states honest. Do not change backend/app_server.py until you have confirmed one owner and the API contract in the log. Codex is not editing either shared core file during this review.

1. The fixed Survey 3 polygon, its approximate area versus the displayed 4 acres, and the “verified/authenticated” labels.
2. Farmer profile claims, privacy/authentication boundary, and whether plot edits persist.
3. The empty AGMARKNET status versus price, yield, cost, freight, suitability, and ROI values returned by recommendations.
4. Whether the dynamic crop endpoint reads knowledge/crops/catalog.json and includes the Dolly/Naavi leads, with stock and evidence clearly separated.
5. The simulated NDVI/Sentinel-2 labels, actual translated screen coverage, voice values, and chemical-safety gate in the production path.
6. Whether the current Python suite exercises the actual live routes and whether the Java/PostGIS layer is used by the active app.

Then append Entry 016 to AGENT_LOG.md with:

- which findings you verified, corrected, or disagree with and the evidence;
- what you completed before your Entry 014 “concluded” status that remains true today;
- your proposed single owner for backend/app_server.py and precise task split for the next phase;
- the farmer-facing changes you recommend first, with acceptance conditions;
- any factual correction to the 10-year approach.

Do not claim the agents agree unless both have explicitly confirmed in the log. Do not invent local seed stock, mandi prices, farmer outcomes, land boundaries, soil tests, partnerships, market-size numbers, or regulatory approvals. Treat daily AGMARKNET observations as dated wholesale records, not live tick prices or a price forecast. Append Entry 016 with your evidence and ownership proposal, then proceed with the frontend-owned corrections above; hold backend edits for an explicit API/ownership handoff.
