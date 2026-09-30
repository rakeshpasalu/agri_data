# Bhumi Intelligence: Product Truth Audit and 10-Year Approach

**Review date:** 30 September 2026  
**Scope:** Live application at localhost:8080, the active Python API, the crop knowledge catalog, and the visible Python test suite. This is a product and data-integrity review, not a field-trial agronomy validation.

## Executive verdict

There is a real product opportunity here: farmers in Molakalmuru need a dependable way to compare crop choices, water needs, input costs, seed options, current market signals, and likely sale routes. Bhumi has useful beginnings: a live weather connection, a safe official-feed integration that refuses to invent prices, a manual Bhoomi verification path, local-language crop names, and a source-aware crop catalog.

The current product is not yet safe to use for planting or investment decisions, and its current investor pitch is not credible. The interface presents precise parcel, soil, yield, mandi, fertilizer, and profit claims that the live services do not establish. The most important market input currently says “setup required” and returns no price observations, while the crop recommendation service still produces confident rankings and rupee returns from fixed code values.

The right next move is to earn trust with a small, measured Hosanagalapura pilot: capture farmer-confirmed plot and input data, use source-dated local market observations, show uncertainty and missing information, and record actual outcomes. Build the farmer decision loop first. “Agricultural operating system” and a unicorn outcome are long-term ambitions, not present-day proof.

## What I verified in the running app

At 13:06 IST on 30 September 2026:

- The health endpoint returned UP.
- Open-Meteo returned an online 14-day forecast for the default point near Hosanagalapura. The Python handler also contains a generated weather fallback; the UI’s label stays “LIVE SYNC” and does not visibly distinguish that fallback.
- The official AGMARKNET service returned setup_required, zero records, and a message that DATA_GOV_IN_API_KEY is needed. This is honest behavior in that route.
- Despite that empty price response, the recommendation endpoint returned crop scores, yields, mandi prices, freight deductions, cultivation costs, and net profit.
- The farmer profile endpoint returned a fixed 4-acre claim, coordinates and elevation, soil series and texture, pH 6.82, and borewell/drip information. Those values need farmer confirmation or measured sources before being displayed as facts.
- The live page rendered six crop cards with match scores from 90% to 99%. Each card’s “66.4 Qntl (4 Ac Total)” sublabel is the same, even when the per-acre yield differs.
- The page’s default language is English. The language switch implementation changes the voice-button label and Bhoomi link and selects translated crop names; most page labels, instructions, and timeline text remain English.

## The roast: critical product issues

### P0 — Financial recommendations are disconnected from live prices

The live price route and recommendation route are separate. Recommendations still use a fixed crop list and fixed base mandi prices in backend/app_server.py. The active endpoint returns exact current-looking rupee values even though the real AGMARKNET endpoint has no rows. The product therefore cannot honestly say a crop is “best based on weather and price” today.

The model also subtracts a fixed freight formula and fixed cost estimates. The code’s straight-line distance multiplied by 1.28 is a rough assumption, not a route calculation or a transport quote. Crop-card wording such as “mandi realization” and “net return” makes these assumptions look like local transactions.

**Consequence:** a farmer could spend money based on a false margin. Until the inputs are sourced and calibrated, suppress ranking-by-profit and all rupee return claims. When data is missing, say what is missing and offer a safe next step.

### P0 — The parcel drawn on the map is invented and the acreage does not match it

The frontend creates a fixed four-corner polygon in code and calls it “YOUR VERIFIED LAND” with an authenticated proprietor. It is not read from Bhoomi, drawn by the farmer, or confirmed by the farmer. The approximate dimensions of those coordinates are 445 m by 430 m, or about 47 acres, not the 4.0 acres shown elsewhere. Clicking the map moves the point marker; it does not reshape or save the parcel.

This conflicts with the explicit rule in AGENT_LOG.md: do not show synthetic cadastral boundaries or pretend Bhoomi verification happened. The safe Bhoomi gateway itself correctly says manual verification is required and returns no owner or boundary.

**Consequence:** remove the polygon and all verified/authenticated boundary wording until a farmer draws or imports a boundary and confirms it. Store the boundary as farmer-provided geometry with provenance and date; keep it visibly distinct from a statutory boundary.

### P0 — Soil and farm inputs look measured but are inferred or fixed

The backend derives pH, organic carbon, N/P/K, texture, and soil depth from a coordinate/elevation heuristic. The profile API separately returns pH 6.82 and a soil series as if these were measured. The screen shows a soil pH control, but its recommendation request only sends latitude, longitude, and water type; changing pH does not send the new pH to the crop service. The screen and profile also show a fixed acreage, GPS point, elevation, and “Borewell (160 LPM) + Drip Ready” claim.

Weather is a real and useful input, but 14 days of forecast cannot establish full-season rainfall, root-zone water, farm soil, farmer costs, or crop performance. The map’s default village point is not a verified field survey.

**Consequence:** label every input by origin: farmer-declared, lab-measured, sensor-observed, government record, forecast, or modeled. Show a measurement date and source. Never use a generalized benchmark as if it were this plot’s test result.

### P0 — Specific crop-protection instructions overstate safety validation

The protocol modal gives chemical names, concentrations, doses, pest claims, and a “CIB&RC Compliance Verified” badge. The visible instructions do not expose the source document, exact product label, registration context, reviewer, or last verification date. A separate safety test that checks a local JSON list is not evidence that this rendered advice came through that gate.

**Consequence:** suppress specific pesticide instructions unless a current, crop-and-pest-specific approved label and an agronomist-reviewed source are attached to that recommendation. Until then, provide identification and escalation guidance, not a dose. Remove statutory-clearance badges that the runtime does not enforce.

### P0 — Identity is presented as authentication; personal data has no visible access boundary

Antigravity’s Entry 014 says the phone number was supplied by the farmer. That makes it a farmer-declared contact, not proof of authentication, account ownership, parcel ownership, or consent to publish it. The live page exposes the number alongside survey details, and the profile endpoint returns it from a fixed profile without an authentication flow.

**Consequence:** treat the number as private contact data, obtain explicit consent for its use, avoid printing or voicing it, and do not use “authenticated proprietor” language unless identity and authorization have actually been verified. Before any network deployment, add proper access control and data minimization.

### P1 — Farmer-prioritized seed leads do not reach the live crop cards

knowledge/crops/catalog.json contains Dolly as a seed-company catalogue lead and Naavi F1 as a retailer catalogue lead, with clear caveats about local performance and stock. backend/app_server.py instead keeps a second crop/variety list in code. That list shows HA-4/HA-3 for field bean and other ridge-gourd varieties; it does not load the evidence-linked catalog, so Dolly and Naavi are missing from the runtime list.

Variety identity, local performance, certified seed lot, dealer stock, and current price are different facts. A catalogue listing must not be promoted to local availability. But it should be visible as a sourced lead if the farmer asks for it, with the limitation explained.

**Consequence:** create one versioned crop/variety data source that the API actually reads. Record aliases in Kannada, Telugu, Hindi, English, and common local/romanized forms. For each seed listing, show evidence type and separately mark trial evidence, packet/lot certification, stock, seller, quote, and last checked time.

### P1 — “NDVI” and “Sentinel-2” language does not match the map layer

The page header claims “SENTINEL-2 & LIVE METEO ACTIVE.” The NDVI control is labelled simulated, but its implementation overlays OpenStreetMap humanitarian tiles on top of the satellite image; it is not a vegetation-index product. Esri World Imagery can be a useful visual basemap, but it does not itself provide crop health, cadastral ownership, or a verified parcel outline.

**Consequence:** remove Sentinel-2/NDVI claims until a dated, cloud-screened satellite vegetation-index product is actually integrated. Keep basemap attribution and distinguish visual imagery from analytical layers.

### P1 — Local-language support is currently a switch, not a translated product

The interface has four language buttons, but its translation dictionary currently covers only the voice button and Bhoomi link. The voice message uses fixed yield and profit figures, includes the phone number in English, and has no Hindi voice branch; non-Kannada/Telugu voice falls through to English. The message can contradict the selected crop and actual API response.

**Consequence:** translate the end-to-end decision flow and have crop/extension terminology reviewed by local speakers. Build speech from the current, source-backed recommendation payload. If there is no safe, reviewed translation or supported voice, say so rather than speaking a false value.

### P1 — The app is optimized to impress a pitch viewer, not help a farmer make one decision

The farmer view contains a VC pitch memo, executive labels, “Digital Twin,” “STCR,” “ET0,” “biophysical,” and “investment portfolio” language. It foregrounds six glossy cards and large return numbers instead of a short answer to: what can I plant now, what is the main risk, what do I need to verify, and where can I sell?

The UI also includes investor-market-size and pilot-ROI claims without citations in the app. The VC memo should be a separate investor artifact, not part of a farmer’s daily workbench.

**Consequence:** design the first screen for a low-bandwidth phone and one high-value task. Use familiar words, voice, clear units, a short action list, and a visible “why / data checked” explanation. Use motion only to explain something real, such as a rain window, a source-dated price trend, or a crop-stage calendar; provide a static, low-bandwidth option and respect reduced-motion settings.

### P1 — The product does not yet close the season loop

The active Python service is a GET-only local server. The farmer page does not persist the farmer’s edits, field pin, acreage, crop choice, expenses, harvest, or sale. A Java/PostGIS-oriented schema exists under backend/src, but the running Python application does not appear to use it.

There is no observed loop from “advice shown” to “advice followed” to “inputs purchased” to “harvest and quality” to “actual sale receipt.” Without this loop, the system cannot validate its yield assumptions or learn which advice helps this locality.

**Consequence:** capture farmer-consented season records in small steps: sowing date and variety/lot, water events, material/labour costs, harvest quantity and grade, buyer/market, sale date and price, and whether advice was followed. Make offline capture and later sync a product requirement, not a future flourish.

### P1 — Current tests do not establish the live service is safe

The Python test files I inspected include local helper implementations of suitability and regulatory decisions rather than requests to the running production handlers. The missing-data test can pass without exercising the current recommendation API that emits crop returns when market data is empty. The shared log’s “15 tests pass” statement therefore should not be read as proof that the live API suppresses unsafe outputs.

**Consequence:** add integration checks against the real application contract: missing price rows must not produce a price-based winner; missing soil test must not generate measured soil facts; declared land must never be returned as authenticated; language selection must cover all visible content; and every displayed number must carry its source and date.

### P1 — Collaboration and change safety need a baseline

I found no Git metadata in this workspace, despite the shared log calling this a repository. A communication log helps avoid conflicts but cannot show a diff, restore a known state, or safely compare parallel changes.

**Consequence:** agree a clean source-control baseline and one owner per shared file before the next code sprint. Keep the single port-8080 server under one named operator and do not restart it without a logged handoff.

## Will the current pitch work?

**As written, no. The product thesis could work; this pitch cannot support it yet.**

An investor or an experienced farmer will ask whether the prices are current, where the yield and soil numbers came from, how many real farmers used the recommendation, whether the farmer followed it, what the sale receipt showed, and whether the outcome was better than the farmer’s normal practice. The current memo answers those questions with fixed assumptions and a modeled “3.2x ROI,” not a documented field outcome. The asserted 140M/$40B problem numbers also need independently sourced definitions and citations before they belong in a pitch.

Remove the pilot cash-flow claim, 3.2x ROI, “zero hallucination,” “live mandi arbitrage,” direct Bhoomi boundary integration, certified local-stock claims, and “Series A” language until each is true and auditable. Do not pitch fake precision as a moat.

The strongest honest early pitch is narrower:

> Bhumi helps farmers in one dry-zone area make and track crop, input, and selling decisions using source-dated local signals. It shows what is known, what is uncertain, and what the farmer should verify. We are measuring whether those decisions improve realized margin and reduce avoidable risk over actual seasons.

That is a testable proposition. It is not yet proof of product-market fit or a unicorn path.

## Best approach: build a trusted farmer decision loop

### 1. Establish one source of truth for every fact

Every value should carry:

- the value and unit;
- its origin: farmer-declared, field/lab measured, official record, government observation, forecast, or model output;
- source link or record ID;
- observed, fetched, or valid-through time;
- location and scope;
- confidence/limitations;
- review or expiry status.

Keep crop profiles and seed listings as versioned evidence-linked data, not duplicated in Python code and JSON. Code should implement general decision rules; evidence-backed crop-specific parameters should live in reviewable data with provenance. Do not hide fallback data behind a “live” label.

### 2. Separate observations, forecasts, and scenarios

- **Mandi observation:** commodity, market, variety/grade, min/modal/max, unit, arrival date, source, fetched time, and freshness. AGMARKNET is a daily observation source, not a tick feed and not a future price forecast.
- **Price forecast:** only after enough dated observations exist for a defensible model. Show horizon, uncertainty range, model version, and back-test performance. Otherwise show trend/history or “not enough history.”
- **Weather:** show forecast source, run/fetch time, horizon, and forecast uncertainty. A 14-day outlook can inform near-term timing, not settle an entire season’s crop profitability.
- **Farm conditions:** show only entered/measured values as plot facts. Keep regional maps and climatology clearly labelled as regional context.
- **Economics:** calculate a scenario only from explicit, editable, source-dated costs, yield ranges, quality/grade assumptions, buyer/market price, and transport quote. When a required input is absent, show an incomplete estimate or no estimate.

### 3. Make a recommendation a transparent shortlist, not a magic winner

First ask for the minimum decision inputs: intended sowing window, crop history/rotation, water source and realistic supply, plot area, soil test or Soil Health Card if available, labour/equipment constraints, risk tolerance, and sale preference. Let the farmer correct all profile details.

Then show a small ranked shortlist with:

- “suitable to consider,” “needs verification,” or “not enough data,” rather than a fake 99% certainty score;
- why it fits or does not fit this plot and season;
- water and labour implications;
- seed varieties as evidence-backed leads, with stock explicitly separate;
- downside scenarios and unknown costs;
- a source/date trail and a way to ask an extension worker.

If the inputs are insufficient, the best answer may be a question or a safe checklist, not a crop recommendation.

### 4. Make the initial pilot measurable

Start with a small farmer cohort in Hosanagalapura/Molakalmuru over one complete crop cycle, with local extension/KVK/Raitha Samparka Kendra/FPO participation where available. Do not claim a production partnership until it exists.

Before the season, record baseline practice, intended crop, water, and planned inputs. During the season, record decisions and whether they were followed. At harvest and sale, record measured yield, grade, costs, buyer, quantity, date, price, and transport. Compare outcomes carefully with a suitable baseline or comparison group; do not attribute weather effects to the app.

Pilot measures should include: share of recommendations with complete provenance; price-feed freshness and market coverage; farmer comprehension; recommendation adoption; advice-related safety incidents; complete actual-cost/harvest/sale records; repeat use next decision window; and measured net-margin/risk outcomes. Treat these as targets to define before the pilot, not results already achieved.

### 5. Build farmer distribution and revenue around trust

Start with a free or low-cost farmer decision service distributed through trusted local channels. Potential later customers could include FPOs, buyers, insurers, lenders, or input networks, but no partner or revenue should be presented as secured until contracted. If a seed seller or buyer pays, clearly disclose it and never let payment secretly determine crop ranking.

Potential later revenue models include organization subscriptions, verified workflow/market tools for FPOs, and transparent marketplace or logistics services. Do not monetize farmer data or sell an undisclosed crop ranking.

## A credible 10-year direction

- **Year 0–1: prove one district workflow.** Make Hosanagalapura the learning site, not the claimed market size. Complete an actual season with local farmer review, current market observations, measured costs/outcomes, local-language comprehension, and a safe escalation route. Stop displaying unsupported profit and parcel claims.
- **Years 1–3: prove repeatability across Molakalmuru/Chitradurga.** Add villages only when the same evidence and onboarding workflow works there. Build the local seed-lot/dealer and buyer/market coverage needed for those villages; measure recommendation calibration by crop and season.
- **Years 3–5: establish a Karnataka operating network.** Partner with extension and farmer organizations, integrate lawful data feeds, and make season records portable. Expand crop coverage only when evidence, language review, and local validation are ready.
- **Years 5–10: scale a farmer-consented agricultural data and service network.** Use longitudinal plot-season-outcome records to improve risk estimates and connect verified services such as buyers, logistics, credit, or insurance with explicit consent and auditability.

A unicorn outcome would require repeatable farmer value, trusted distribution, strong retention, defensible outcome data, and a scalable business model. It cannot be inferred from an animated dashboard or a large India-wide farmer count. Treat it as an ambition that the pilot may validate or reject.

## Motion and interaction that would earn their place

Keep motion graphics tied to a real decision:

- animate the forecast window and rainfall confidence around a sowing decision;
- show a price-history line with dated observations, missing days, and confidence;
- reveal crop stages along a calendar, with farmer-confirmed dates;
- explain a water budget only if the farmer has given source capacity and irrigation information.

Avoid animated “radar,” artificial NDVI, pulsing parcel boundaries, and financial counters when they are not backed by corresponding data. Motion must not mask uncertainty or delay the core task; provide reduced-motion and low-bandwidth modes.

## Proposed next ownership split for the shared log

This is a proposal for Antigravity to confirm or amend; it is not a claim that Antigravity has agreed.

- **Codex:** own the evidence/data contract, catalog-to-runtime integration, market-data semantics, recommendation gating, and integration-level acceptance criteria. Do not alter Antigravity’s UI or the active server file until the shared log confirms transfer/ownership.
- **Antigravity:** own farmer-first screen redesign, remove unsupported display claims, full-flow English/Kannada/Telugu/Hindi experience, usable farmer-entered profile and parcel flow, and useful motion/low-bandwidth behavior.
- **Joint decision before core edits:** assign exactly one owner to backend/app_server.py. Antigravity currently owns it per the existing table. Confirm whether that ownership transfers to Codex for backend data integrity, or remains with Antigravity while Codex provides isolated modules and a written API contract.
- **Both:** agree on one recommendation API contract and provenance vocabulary, then test the actual running routes and screen states together. No one should change or restart the shared 8080 service during the other agent’s active verification.

## Launch gates before a farmer relies on Bhumi

1. No fabricated boundary, owner, acreage, soil test, water capacity, current price, yield, or net-return claim.
2. Recommendations receive the same source-backed inputs shown to the farmer; missing critical inputs cause a transparent hold or question.
3. Current price and historical forecast are distinct features with dates, coverage, and uncertainty.
4. Seed identity, performance evidence, certified packet, dealer stock, and quote have separate statuses.
5. Chemical advice is sourced, label-specific, reviewed, and enforced by the production endpoint—or withheld.
6. A farmer can edit, understand, and later recover their profile, plot, and season records, with consent and access controls.
7. The full interface and voice flow are locally reviewed; no spoken values contradict the screen.
8. Integration tests exercise the actual service and verify graceful failure, rather than only reimplementing business rules in test helpers.
9. A pilot records actual adoption and sale outcomes before the product claims economic impact.
