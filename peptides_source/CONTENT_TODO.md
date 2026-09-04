# Peptide content enrichment TODO

All 75 peptide files now have drafted content. Everything below has been schema-validated,
had every citation URL checked, and round-tripped through a real local
`seed.py` → `uvicorn` → `scripts/load_all.py` run (75 loaded, 0 failed). **Nothing has been
pushed to the live service yet** — this is a first-draft-content pass, not a publish.

## Fields covered per peptide

Per `_template.yaml`: `mechanism_of_action`, `quick_start_guide`, `pharmacokinetics`,
`research_indications`, `quality_indicators`, `what_to_expect`, `side_effects_common`,
`safety_notes`, `references`, `research_protocols`. Fields were intentionally omitted
wherever real information didn't exist rather than guessed — see the "needs a closer look"
flags below for where that happened most.

## Workflow per peptide

1. Review `peptides_source/<slug>.yaml`.
2. Push the update: `python scripts/add_peptide.py peptides_source/<slug>.yaml --update --api-url <api-url>`
3. Publish when satisfied: `python scripts/publish_peptide.py <slug> --api-url <api-url>`

## ⚠️ Priority review items

- **dihexa.yaml** — Foundational HGF/c-Met mechanism papers from the compound's own
  Washington State University lab were retracted in 2025 for fabricated data (independently
  confirmed). No references included; safety_notes discloses this in detail. Worth a careful
  read given how consequential the claim is.
- **adipotide.yaml** — Documented kidney-toxicity signal in both the primate study and the
  small human trial; safety_notes is deliberately blunt about this.
- **wolverine-stack.yaml, glow-blend.yaml, klow-blend.yaml, cjc-1295-plus-ipamorelin.yaml,
  semax-plus-selank-blend.yaml** — Combination products. Mechanism described as the sum of
  each component's individually-studied mechanism; safety_notes states the blend itself was
  never independently studied. No references (would misleadingly imply the blend was studied).
- **lipo-b.yaml, lipo-c.yaml, lipo-c-fat-blaster.yaml, super-shred.yaml** — Vendor/commercial
  blend products with no standardized formula and no independent literature. Deliberately thin
  (fewer fields filled) rather than asserting a formula or dose as standard.
- **snap-8.yaml** — The only findable "SNAP-8" citation turned out to be about a different
  peptide (Argireline) on closer check, so no references were included.
- **thymogen.yaml, vilon.yaml, foxo4-dri.yaml, pinealon.yaml, p21.yaml, adamax.yaml,
  ara-290.yaml** (Khavinson-school bioregulators, or otherwise very early-stage compounds) —
  little to no human data exists; dosing/PK fields are explicitly marked "not established"
  rather than filled with vendor-forum numbers.
- **ovagen.yaml** — the Trello source list assumed this was an ovarian/reproductive bioregulator
  based on the name; every independent source instead describes it as a liver/GI compound
  ("для печени и ЖКТ"). The actual Khavinson ovarian-targeted product is a separately named
  preparation ("Zhenoluten") not on the list at all. Filed under its real (liver/GI) target;
  overview and safety_notes call out the naming trap directly.
- **cartalax.yaml** — marketed for cartilage/joint support, but none of its indexed studies test
  a cartilage endpoint at all (kidney, skin, thymus, and stem-cell studies only) — the gap
  between the marketing claim and the actual evidence base is stated plainly rather than
  glossed over.
- **gdf-8-myostatin.yaml** — GDF-8 is Myostatin itself, the muscle-growth-*limiting* factor, not
  a booster. Written honestly as such (cross-referencing `follistatin-344.yaml`, which covers
  the inhibitor side); no `research_protocols` section, since no legitimate human dosing
  protocol exists for administering more of it.
- **pnc-27.yaml** — early-stage anticancer research peptide with essentially no human safety
  data. safety_notes includes a real reported fatality from off-protocol use, included
  deliberately rather than downplayed given how consequential that is.
- **ibutamoren.yaml** (MK-677) — the pivotal elderly-population trial (Adunsky et al. 2011) was
  halted early over a congestive-heart-failure safety signal (6.5% vs. 1.7% placebo); flagged
  prominently in safety_notes rather than buried under the growth-hormone benefits.
- **tesofensine.yaml** — not FDA-approved anywhere; the foundational 2008 trial carries an
  unresolved 2013 Lancet Expression of Concern over under-reported adverse events at 2 of 5
  study sites. Stated plainly, cited from Retraction Watch and The Lancet directly.
- **os-01-face-peptide.yaml / atx-304.yaml** — the Trello card listed these as one item
  ("OS-01 (O-304/ATX-304)"), but they're two unrelated compounds (OneSkin's cosmetic peptide
  vs. an unrelated AMPK-activator small molecule) accidentally conflated by at least one vendor
  page. Split into two separate entries; each notes why.
- **rapamycin.yaml** — FDA-approved prescription immunosuppressant used off-label for
  longevity research; safety_notes separates the well-characterized transplant-dose risk
  profile from the much thinner low-dose/off-label longevity safety data, and states the
  prescription-only status directly (same treatment as Semaglutide/Tirzepatide).
- **ptd-dbm.yaml, pnc-27.yaml, bronchogen.yaml, chonluten.yaml, vesugen.yaml, cartalax.yaml,
  ovagen.yaml, pancragen.yaml** — no existing category fits cleanly (no hair, oncology,
  respiratory, cardiovascular, or pancreas/liver category exists in the lookup table); each was
  filed under the closest available category with the mismatch noted in-file as a comment.
- **"Formula N-69/N-111/N-259/N-2331/N-5550/RG-5555/WL-6250" and "Glow Core/Plus/Ultra"** —
  investigated, not drafted. The seven "Formula" codes traced to a single site whose own
  about-page describes its content as AI-generated, with zero independent corroboration from
  any real vendor — treated as unverifiable rather than fabricated into entries. The three
  "Glow" tiers turned out to be the same or non-novel-dosage variants of the existing
  `glow-blend.yaml`/`klow-blend.yaml` recipes, per the same single unreliable source — no new
  entries needed.
- **EPO, Dermorphin** — deliberately not researched or drafted. Both are qualitatively riskier
  than anything else in the encyclopedia (EPO: banned blood-doping agent; Dermorphin: a
  frog-venom-derived opioid ~30–40x morphine's potency, banned in horse racing) — held back
  pending the same Play policy review already gating GLP-1 inclusion elsewhere in this project.

## Peptides (grouped by category)

### Healing & Recovery
- [x] **BPC-157** — [`bpc-157.yaml`](./bpc-157.yaml)
- [x] **TB-500** — [`tb-500.yaml`](./tb-500.yaml)
- [x] **KPV** — [`kpv.yaml`](./kpv.yaml)
- [x] **ARA-290** — [`ara-290.yaml`](./ara-290.yaml) — sparse human data, flagged above
- [x] **TB-500 (Frag)** — [`tb-500-frag.yaml`](./tb-500-frag.yaml)
- [x] **Wolverine Stack** — [`wolverine-stack.yaml`](./wolverine-stack.yaml) — combo, flagged above
- [x] **GLOW Blend** — [`glow-blend.yaml`](./glow-blend.yaml) — combo, flagged above
- [x] **KLOW Blend** — [`klow-blend.yaml`](./klow-blend.yaml) — combo, flagged above

### Growth Hormone & Growth Factors
- [x] **CJC-1295** — [`cjc-1295.yaml`](./cjc-1295.yaml)
- [x] **Ipamorelin** — [`ipamorelin.yaml`](./ipamorelin.yaml)
- [x] **GHRP-2** — [`ghrp-2.yaml`](./ghrp-2.yaml)
- [x] **GHRP-6** — [`ghrp-6.yaml`](./ghrp-6.yaml)
- [x] **Sermorelin** — [`sermorelin.yaml`](./sermorelin.yaml)
- [x] **Tesamorelin** — [`tesamorelin.yaml`](./tesamorelin.yaml)
- [x] **Hexarelin** — [`hexarelin.yaml`](./hexarelin.yaml)
- [x] **IGF-1 LR3** — [`igf-1-lr3.yaml`](./igf-1-lr3.yaml)
- [x] **MGF** — [`mgf.yaml`](./mgf.yaml)
- [x] **PEG-MGF** — [`peg-mgf.yaml`](./peg-mgf.yaml)
- [x] **ACE-031** — [`ace-031.yaml`](./ace-031.yaml)
- [x] **CJC-1295 (with DAC)** — [`cjc-1295-with-dac.yaml`](./cjc-1295-with-dac.yaml)
- [x] **CJC-1295 + Ipamorelin** — [`cjc-1295-plus-ipamorelin.yaml`](./cjc-1295-plus-ipamorelin.yaml) — combo, flagged above
- [x] **HGH** — [`hgh.yaml`](./hgh.yaml)
- [x] **HGH Frag 176-191** — [`hgh-frag-176-191.yaml`](./hgh-frag-176-191.yaml)

### Metabolic & Weight Management
- [x] **AOD-9604** — [`aod-9604.yaml`](./aod-9604.yaml)
- [x] **Semaglutide** — [`semaglutide.yaml`](./semaglutide.yaml)
- [x] **Tirzepatide** — [`tirzepatide.yaml`](./tirzepatide.yaml)
- [x] **Retatrutide** — [`retatrutide.yaml`](./retatrutide.yaml)
- [x] **Cagrilintide** — [`cagrilintide.yaml`](./cagrilintide.yaml)
- [x] **Liraglutide** — [`liraglutide.yaml`](./liraglutide.yaml)
- [x] **Survodutide** — [`survodutide.yaml`](./survodutide.yaml)
- [x] **5-Amino-1MQ** — [`5-amino-1mq.yaml`](./5-amino-1mq.yaml)
- [x] **Adipotide** — [`adipotide.yaml`](./adipotide.yaml) — toxicity signal, flagged above
- [x] **AICAR** — [`aicar.yaml`](./aicar.yaml)
- [x] **L-Carnitine** — [`l-carnitine.yaml`](./l-carnitine.yaml)
- [x] **Lipo-B** — [`lipo-b.yaml`](./lipo-b.yaml) — vendor blend, flagged above
- [x] **Lipo-C** — [`lipo-c.yaml`](./lipo-c.yaml) — vendor blend, flagged above
- [x] **Lipo-C Fat Blaster** — [`lipo-c-fat-blaster.yaml`](./lipo-c-fat-blaster.yaml) — vendor blend, flagged above
- [x] **Super Shred** — [`super-shred.yaml`](./super-shred.yaml) — vendor blend, flagged above

### Cognitive & Neuroprotective
- [x] **Semax** — [`semax.yaml`](./semax.yaml)
- [x] **Selank** — [`selank.yaml`](./selank.yaml)
- [x] **Dihexa** — [`dihexa.yaml`](./dihexa.yaml) — **retraction disclosure, flagged above**
- [x] **Cerebrolysin** — [`cerebrolysin.yaml`](./cerebrolysin.yaml)
- [x] **Pinealon** — [`pinealon.yaml`](./pinealon.yaml) — sparse data, flagged above
- [x] **P21** — [`p21.yaml`](./p21.yaml) — sparse data, flagged above
- [x] **Adamax** — [`adamax.yaml`](./adamax.yaml) — sparse data, flagged above
- [x] **PE 22-28** — [`pe-22-28.yaml`](./pe-22-28.yaml)
- [x] **VIP** — [`vip.yaml`](./vip.yaml)
- [x] **Semax + Selank Blend** — [`semax-plus-selank-blend.yaml`](./semax-plus-selank-blend.yaml) — combo, flagged above

### Longevity & Cellular Health
- [x] **Epithalon** — [`epithalon.yaml`](./epithalon.yaml)
- [x] **MOTS-c** — [`mots-c.yaml`](./mots-c.yaml)
- [x] **Humanin** — [`humanin.yaml`](./humanin.yaml)
- [x] **SS-31** — [`ss-31.yaml`](./ss-31.yaml)
- [x] **FOXO4-DRI** — [`foxo4-dri.yaml`](./foxo4-dri.yaml) — sparse data, flagged above
- [x] **Thymalin** — [`thymalin.yaml`](./thymalin.yaml)
- [x] **Vilon** — [`vilon.yaml`](./vilon.yaml) — sparse data, flagged above
- [x] **NAD+** — [`nad-plus.yaml`](./nad-plus.yaml)
- [x] **Glutathione** — [`glutathione.yaml`](./glutathione.yaml)

### Sexual Health
- [x] **PT-141** — [`pt-141.yaml`](./pt-141.yaml)
- [x] **Melanotan II** — [`melanotan-ii.yaml`](./melanotan-ii.yaml)
- [x] **Kisspeptin-10** — [`kisspeptin-10.yaml`](./kisspeptin-10.yaml)
- [x] **Gonadorelin** — [`gonadorelin.yaml`](./gonadorelin.yaml)
- [x] **HCG** — [`hcg.yaml`](./hcg.yaml)
- [x] **HMG** — [`hmg.yaml`](./hmg.yaml)

### Immune & Inflammation
- [x] **Thymosin Alpha-1** — [`thymosin-alpha-1.yaml`](./thymosin-alpha-1.yaml)
- [x] **LL-37** — [`ll-37.yaml`](./ll-37.yaml)
- [x] **Thymogen** — [`thymogen.yaml`](./thymogen.yaml) — sparse data, flagged above

### Sleep & Relaxation
- [x] **DSIP** — [`dsip.yaml`](./dsip.yaml)

### Skin & Anti-Aging
- [x] **GHK-Cu** — [`ghk-cu.yaml`](./ghk-cu.yaml)
- [x] **Melanotan I** — [`melanotan-i.yaml`](./melanotan-i.yaml)
- [x] **AHK-Cu** — [`ahk-cu.yaml`](./ahk-cu.yaml)
- [x] **SNAP-8** — [`snap-8.yaml`](./snap-8.yaml) — citation mismatch found and avoided, flagged above
- [x] **Matrixyl** — [`matrixyl.yaml`](./matrixyl.yaml)
- [x] **Botulinum Toxin** — [`botulinum-toxin.yaml`](./botulinum-toxin.yaml)
- [x] **Hyaluronic Acid** — [`hyaluronic-acid.yaml`](./hyaluronic-acid.yaml)

### Bone & Structural Health
- [x] **Teriparatide** — [`teriparatide.yaml`](./teriparatide.yaml)

---

**Progress: 75 / 75 drafted. 0 / 75 published to the live service.**

## Batch 2 — added 2026-08-11

12 new peptides, drafted following the same workflow and citation-verification rigor as the
original 75 (schema-validated; every citation independently confirmed via WebSearch/WebFetch
before inclusion; omitted rather than guessed where real evidence didn't exist). Round-tripped
through a local seed/load test (87/87 loaded, 0 failed), then pushed and published to the live
service.

- [x] **Bioglutide (NA-931)** — [`bioglutide.yaml`](./bioglutide.yaml) — investigational, not a
  peptide (small molecule); no peer-reviewed publication exists yet, only company conference
  presentations — references deliberately omitted, see safety_notes.
- [x] **Eloralintide** — [`eloralintide.yaml`](./eloralintide.yaml) — investigational Lilly amylin
  agonist; cited from its Molecular Metabolism discovery paper and the Lancet Phase 2 trial.
- [x] **Mazdutide** — [`mazdutide.yaml`](./mazdutide.yaml) — investigational GLP-1/glucagon dual
  agonist; cited from its Phase 1b (eClinicalMedicine) and Phase 2 (Nature Communications) trials.
- [x] **Orforglipron** — [`orforglipron.yaml`](./orforglipron.yaml) — not a peptide (small molecule);
  now FDA-approved (Foundayo, 2026) — the one entry in this batch describing an approved drug
  rather than a research/investigational compound.
- [x] **Cyclic Glycine-Proline (cGP)** — [`cyclic-glycine-proline.yaml`](./cyclic-glycine-proline.yaml)
  — sparse data, single New Zealand research group, no human dosing established.
- [x] **Follistatin 344** — [`follistatin-344.yaml`](./follistatin-344.yaml) — the only real clinical
  data on this exact isoform is a small AAV gene-therapy trial in Becker muscular dystrophy, a
  different route/mechanism than the injectable protein vendors sell; safety_notes is explicit
  about that gap.
- [x] **Adalank (N-Acetyl Selank Amidate)** — [`adalank.yaml`](./adalank.yaml) — no published studies
  of this analog itself exist; content is explicit that pharmacology is extrapolated from Selank.
- [x] **Bromantane** — [`bromantane.yaml`](./bromantane.yaml) — not a peptide (small molecule);
  Russian-approved (Ladasten) actoprotector; WADA-banned, noted in safety_notes.
- [x] **NA Semax Amidate** — [`na-semax-amidate.yaml`](./na-semax-amidate.yaml) — no published
  studies of this analog itself exist; content is explicit that pharmacology is extrapolated from
  Semax (same treatment as Adalank/Selank above).
- [x] **Omberacetam (Noopept)** — [`omberacetam.yaml`](./omberacetam.yaml) — oral, not injected;
  Russian-registered nootropic, cited from Gudasheva's original synthesis paper and Ostrovskaya's
  NGF/BDNF mechanism paper.
- [x] **Cardiogen** — [`cardiogen.yaml`](./cardiogen.yaml) — Khavinson-school bioregulator, sparse
  data (single tissue-culture study), same treatment as Vilon/Thymalin above.
- [x] **Livagen** — [`livagen.yaml`](./livagen.yaml) — Khavinson-school bioregulator, sparse data
  (cell-culture and animal studies only), same treatment as Vilon/Thymalin above.

**Batch 2 progress: 12 / 12 drafted and published to the live service.**

## Batch 3 — reconstitution mixers, added 2026-08-17

Not peptides — added per Trello card "Add Mixers" so the app's Encyclopedia/Mixology screens
have a real backing entry for the two diluents peptide protocols actually call for. Dosing/PK/
research-protocol fields intentionally omitted throughout (a diluent has no dose or half-life of
its own). New category `reconstitution-mixers` added to `seed.py` — must be created live via
`POST /categories` before these can be pushed with `add_peptide.py` (category_ids are validated
against the lookup table). **Drafted only — not yet pushed/published; needs `ADMIN_API_KEY`.**

- [ ] **Bacteriostatic Water** — [`bacteriostatic-water.yaml`](./bacteriostatic-water.yaml) —
  FDA DailyMed label cited (0.9% benzyl alcohol, USP). Vial sizes 3/10/30 mL per the Trello card.
- [ ] **Acetic Acid** — [`acetic-acid.yaml`](./acetic-acid.yaml) — no independent literature on
  this as a peptide-reconstitution mixer specifically (it's a vendor/community convention, mainly
  for Melanotan I/II solubility); no references included, same treatment as the vendor-blend
  entries above. Vial sizes 3/10/12 mL per the Trello card.
- Per the card: Saline and Sterile Water exist on the market but no peptide protocol found calls
  for them specifically as a reconstitution mixer, so they were deliberately not added here.

## Batch 4 — Trello "new peptides to add" card, added 2026-09-05

34 new entries, researched and drafted by five parallel agents against the same citation-
verification rigor as prior batches (every reference confirmed to a real, findable source before
inclusion; omitted rather than guessed where evidence didn't exist). Two existing entries
(`omberacetam.yaml`, `dsip.yaml`) got `aliases` added instead of duplicate files — see below.
Pushed to the live service and published 2026-09-05. See "Priority review items" above for the
most consequential per-entry flags.

- [x] **Fisetin** — [`fisetin.yaml`](./fisetin.yaml)
- [x] **N-Acetyl Cysteine (NAC)** — [`n-acetyl-cysteine.yaml`](./n-acetyl-cysteine.yaml)
- [x] **NMN** — [`nmn.yaml`](./nmn.yaml)
- [x] **Pterostilbene** — [`pterostilbene.yaml`](./pterostilbene.yaml)
- [x] **Quercetin** — [`quercetin.yaml`](./quercetin.yaml)
- [x] **Resveratrol** — [`resveratrol.yaml`](./resveratrol.yaml)
- [x] **Spermidine** — [`spermidine.yaml`](./spermidine.yaml)
- [x] **Rapamycin** — [`rapamycin.yaml`](./rapamycin.yaml) — prescription drug, flagged above
- [x] **Alpha-GPC** — [`alpha-gpc.yaml`](./alpha-gpc.yaml) — cites a 2021 JAMA Network Open
  cohort study linking use to higher stroke risk via gut-derived TMAO
- [x] **GDF-11** — [`gdf-11.yaml`](./gdf-11.yaml) — contested field (2014 *Science* rejuvenation
  claim directly contradicted by a 2015 *Cell Metabolism* paper); both sides cited
- [x] **GDF-8 (Myostatin)** — [`gdf-8-myostatin.yaml`](./gdf-8-myostatin.yaml) — flagged above
- [x] **OS-01 (OneSkin Peptide)** — [`os-01-face-peptide.yaml`](./os-01-face-peptide.yaml) — split
  from ATX-304, flagged above
- [x] **ATX-304 (O-304)** — [`atx-304.yaml`](./atx-304.yaml) — split from OS-01, flagged above
- [x] **SLU-PP-332** — [`slu-pp-332.yaml`](./slu-pp-332.yaml) — animal-only evidence, no human data
- [x] **N-Acetyl Epitalon Amidate** — [`na-epitalon-amidate.yaml`](./na-epitalon-amidate.yaml) —
  no independent study of the analog itself exists; pharmacology extrapolated from base
  Epithalon, same treatment as Adalank/NA-Semax-Amidate
- [x] **Ibutamoren (MK-677)** — [`ibutamoren.yaml`](./ibutamoren.yaml) — the source list had this
  twice under two different names; one entry, flagged above
- [x] **Des(1-3)IGF-1** — [`des-1-3-igf-1.yaml`](./des-1-3-igf-1.yaml) — the source list's
  "IDF-DES" shorthand resolved to this compound; filed under its real name
- [x] **Bronchogen** — [`bronchogen.yaml`](./bronchogen.yaml) — Khavinson bioregulator, sparse
  data, category mismatch flagged above
- [x] **Cartalax** — [`cartalax.yaml`](./cartalax.yaml) — Khavinson bioregulator, evidence gap
  flagged above
- [x] **Chonluten** — [`chonluten.yaml`](./chonluten.yaml) — Khavinson bioregulator, sparse data,
  category mismatch flagged above
- [x] **Cortagen** — [`cortagen.yaml`](./cortagen.yaml) — Khavinson bioregulator, sparse data
- [x] **Crystagen** — [`crystagen.yaml`](./crystagen.yaml) — Khavinson bioregulator, sparse data
- [x] **Ovagen** — [`ovagen.yaml`](./ovagen.yaml) — Khavinson bioregulator, mislabeled-target
  correction flagged above
- [x] **Pancragen** — [`pancragen.yaml`](./pancragen.yaml) — Khavinson bioregulator, category
  mismatch flagged above
- [x] **Prostamax** — [`prostamax.yaml`](./prostamax.yaml) — Khavinson bioregulator, sparse data
- [x] **Testagen** — [`testagen.yaml`](./testagen.yaml) — Khavinson bioregulator; its one human
  trial used oral capsules, not an injectable — noted in-file
- [x] **Vesugen** — [`vesugen.yaml`](./vesugen.yaml) — Khavinson bioregulator, category mismatch
  flagged above
- [x] **Cortexin** — [`cortexin.yaml`](./cortexin.yaml) — Khavinson bioregulator, sparse Western
  data
- [x] **Ptd-DBM** — [`ptd-dbm.yaml`](./ptd-dbm.yaml) — real preclinical compound (Choi lab,
  Yonsei University), no human data, category mismatch flagged above
- [x] **Oxytocin** — [`oxytocin.yaml`](./oxytocin.yaml) — distinguishes FDA-approved injectable
  (obstetric) from unapproved intranasal research use
- [x] **Zinc-Thymulin** — [`zinc-thymulin.yaml`](./zinc-thymulin.yaml) — human dosing not
  established
- [x] **Tesofensine** — [`tesofensine.yaml`](./tesofensine.yaml) — unresolved trial concern
  flagged above
- [x] **PNC-27** — [`pnc-27.yaml`](./pnc-27.yaml) — fatality case report, category mismatch,
  both flagged above
- [x] **Semaglutide + BPC-157** — [`semaglutide-plus-bpc-157.yaml`](./semaglutide-plus-bpc-157.yaml)
  — new combo blend, same treatment as GLOW/KLOW Blend (combination unstudied as a unit, no
  references section)

**Aliased into existing entries, not duplicated:**
- **Noopept** → added as an alias on [`omberacetam.yaml`](./omberacetam.yaml) (same compound;
  Omberacetam is the INN, Noopept the trade name)
- **Emideltide** → added as an alias on [`dsip.yaml`](./dsip.yaml) (same compound, same CAS
  number, alternate INN-style name)

**Not drafted — see "Priority review items" above for why:** the seven "Formula N-XX/RG-5555/
WL-6250" codes (unverifiable, sole source an AI-content site), Glow Core/Plus/Ultra (non-novel
variants of existing GLOW/KLOW), EPO, and Dermorphin (both held for a Play policy decision).

**Batch 4 progress: 34 / 34 drafted and published to the live service.**

