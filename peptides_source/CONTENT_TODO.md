# Peptide content enrichment TODO

74 of the 75 peptide files only have `overview`, `key_benefits`, and (where available)
`reconstitution_steps` — migrated from the old Android app's free-text list. Everything
else the schema supports is still missing. `bpc-157.yaml` is the one exception (fully
authored) — open it alongside `_template.yaml` as a reference for tone/format.

## Fields to fill in per peptide

Per `_template.yaml`, add whatever applies (skip what genuinely isn't known — omit the
field rather than guessing):

- [ ] `mechanism_of_action` — how it's believed to work, in plain language
- [ ] `quick_start_guide` — `typical_dose`, `frequency`, `injection_site_ids`, `best_timing`, `effects_timeline`, `storage`, `cycle_length`, `break_between`
- [ ] `pharmacokinetics` — `peak`, `half_life`, `cleared`
- [ ] `research_indications` — list of studied indications
- [ ] `quality_indicators` — what a legitimate vial/vendor looks like
- [ ] `what_to_expect` — realistic timeline narrative
- [ ] `side_effects_common` — list
- [ ] `safety_notes` — disclaimers, limited-human-data caveats
- [ ] `references` — `citation` + `url`
- [ ] `research_protocols` — one or more `goal`/`dose`/`timing`/`disclaimer`

*(That's a per-field checklist to copy/reuse per peptide if useful — the real tracking is the per-peptide list below.)*

## Workflow per peptide

1. Edit `peptides_source/<slug>.yaml`, filling in the fields above.
2. Push the update: `python scripts/add_peptide.py peptides_source/<slug>.yaml --update --api-url <api-url>`
3. Check it off below and commit the YAML change.

## Peptides to enrich (grouped by category)

### Healing & Recovery
- [x] **BPC-157** — [`bpc-157.yaml`](./bpc-157.yaml) — reference example, already done
- [ ] **TB-500** — [`tb-500.yaml`](./tb-500.yaml) — _Recovery and flexibility_
- [ ] **KPV** — [`kpv.yaml`](./kpv.yaml) — _Anti-inflammatory tripeptide_
- [ ] **ARA-290** — [`ara-290.yaml`](./ara-290.yaml) — _Tissue-protective erythropoietin fragment (Cibinetide)_
- [ ] **TB-500 (Frag)** — [`tb-500-frag.yaml`](./tb-500-frag.yaml) — _Active fragment of Thymosin Beta-4_
- [ ] **Wolverine Stack** — [`wolverine-stack.yaml`](./wolverine-stack.yaml) — _BPC-157 and TB-500 combination blend_
- [ ] **GLOW Blend** — [`glow-blend.yaml`](./glow-blend.yaml) — _BPC-157, GHK-Cu, and TB-500 combination blend_
- [ ] **KLOW Blend** — [`klow-blend.yaml`](./klow-blend.yaml) — _BPC-157, GHK-Cu, TB-500, and KPV combination blend_

### Growth Hormone & Growth Factors
- [ ] **CJC-1295** — [`cjc-1295.yaml`](./cjc-1295.yaml) — _Growth hormone support_
- [ ] **Ipamorelin** — [`ipamorelin.yaml`](./ipamorelin.yaml) — _Selective growth hormone secretagogue_
- [ ] **GHRP-2** — [`ghrp-2.yaml`](./ghrp-2.yaml) — _Growth hormone releasing peptide_
- [ ] **GHRP-6** — [`ghrp-6.yaml`](./ghrp-6.yaml) — _Growth hormone releasing peptide with strong appetite stimulation_
- [ ] **Sermorelin** — [`sermorelin.yaml`](./sermorelin.yaml) — _GHRH analog_
- [ ] **Tesamorelin** — [`tesamorelin.yaml`](./tesamorelin.yaml) — _GHRH analog studied for visceral fat reduction_
- [ ] **Hexarelin** — [`hexarelin.yaml`](./hexarelin.yaml) — _Potent GH secretagogue_
- [ ] **IGF-1 LR3** — [`igf-1-lr3.yaml`](./igf-1-lr3.yaml) — _Long-acting insulin-like growth factor_
- [ ] **MGF** — [`mgf.yaml`](./mgf.yaml) — _IGF-1 splice variant (Mechano Growth Factor)_
- [ ] **PEG-MGF** — [`peg-mgf.yaml`](./peg-mgf.yaml) — _PEGylated Mechano Growth Factor_
- [ ] **ACE-031** — [`ace-031.yaml`](./ace-031.yaml) — _Myostatin-blocking fusion protein_
- [ ] **CJC-1295 (with DAC)** — [`cjc-1295-with-dac.yaml`](./cjc-1295-with-dac.yaml) — _Extended-release GHRH analog with Drug Affinity Complex_
- [ ] **CJC-1295 + Ipamorelin** — [`cjc-1295-plus-ipamorelin.yaml`](./cjc-1295-plus-ipamorelin.yaml) — _Combined GHRH/ghrelin-mimetic secretagogue stack_
- [ ] **HGH** — [`hgh.yaml`](./hgh.yaml) — _Recombinant human growth hormone_
- [ ] **HGH Frag 176-191** — [`hgh-frag-176-191.yaml`](./hgh-frag-176-191.yaml) — _Fat-burning fragment of human growth hormone_

### Metabolic & Weight Management
- [ ] **AOD-9604** — [`aod-9604.yaml`](./aod-9604.yaml) — _Fat-loss support_
- [ ] **Semaglutide** — [`semaglutide.yaml`](./semaglutide.yaml) — _GLP-1 receptor agonist_
- [ ] **Tirzepatide** — [`tirzepatide.yaml`](./tirzepatide.yaml) — _Dual GIP/GLP-1 receptor agonist_
- [ ] **Retatrutide** — [`retatrutide.yaml`](./retatrutide.yaml) — _Triple GIP/GLP-1/glucagon receptor agonist_
- [ ] **Cagrilintide** — [`cagrilintide.yaml`](./cagrilintide.yaml) — _Long-acting amylin analog_
- [ ] **Liraglutide** — [`liraglutide.yaml`](./liraglutide.yaml) — _GLP-1 receptor agonist_
- [ ] **Survodutide** — [`survodutide.yaml`](./survodutide.yaml) — _Dual GLP-1/glucagon receptor agonist_
- [ ] **5-Amino-1MQ** — [`5-amino-1mq.yaml`](./5-amino-1mq.yaml) — _NNMT enzyme inhibitor_
- [ ] **Adipotide** — [`adipotide.yaml`](./adipotide.yaml) — _Fat-cell vasculature targeting compound_
- [ ] **AICAR** — [`aicar.yaml`](./aicar.yaml) — _AMPK-activating compound_
- [ ] **L-Carnitine** — [`l-carnitine.yaml`](./l-carnitine.yaml) — _Amino-acid derivative supporting fat transport_
- [ ] **Lipo-B** — [`lipo-b.yaml`](./lipo-b.yaml) — _Injectable lipotropic B-vitamin blend_
- [ ] **Lipo-C** — [`lipo-c.yaml`](./lipo-c.yaml) — _Injectable lipotropic blend with vitamin C_
- [ ] **Lipo-C Fat Blaster** — [`lipo-c-fat-blaster.yaml`](./lipo-c-fat-blaster.yaml) — _Injectable lipotropic blend_
- [ ] **Super Shred** — [`super-shred.yaml`](./super-shred.yaml) — _Advanced fat-burning injectable blend_

### Cognitive & Neuroprotective
- [ ] **Semax** — [`semax.yaml`](./semax.yaml) — _Nootropic peptide derived from ACTH_
- [ ] **Selank** — [`selank.yaml`](./selank.yaml) — _Anxiolytic peptide related to tuftsin_
- [ ] **Dihexa** — [`dihexa.yaml`](./dihexa.yaml) — _Neurogenic compound studied for synaptic health_
- [ ] **Cerebrolysin** — [`cerebrolysin.yaml`](./cerebrolysin.yaml) — _Neuropeptide preparation studied for cognitive recovery_
- [ ] **Pinealon** — [`pinealon.yaml`](./pinealon.yaml) — _Short peptide bioregulator_
- [ ] **P21** — [`p21.yaml`](./p21.yaml) — _Neurogenesis-promoting peptide_
- [ ] **Adamax** — [`adamax.yaml`](./adamax.yaml) — _Adamantane-modified nootropic peptide_
- [ ] **PE 22-28** — [`pe-22-28.yaml`](./pe-22-28.yaml) — _BDNF-pathway peptide_
- [ ] **VIP** — [`vip.yaml`](./vip.yaml) — _Vasoactive Intestinal Peptide_
- [ ] **Semax + Selank Blend** — [`semax-plus-selank-blend.yaml`](./semax-plus-selank-blend.yaml) — _Combined Semax and Selank blend (10mg + 10mg)_

### Longevity & Cellular Health
- [ ] **Epithalon** — [`epithalon.yaml`](./epithalon.yaml) — _Telomerase-activating tetrapeptide_
- [ ] **MOTS-c** — [`mots-c.yaml`](./mots-c.yaml) — _Mitochondrial-derived peptide_
- [ ] **Humanin** — [`humanin.yaml`](./humanin.yaml) — _Mitochondrial-derived peptide with cytoprotective effects_
- [ ] **SS-31** — [`ss-31.yaml`](./ss-31.yaml) — _Mitochondria-targeted peptide (Elamipretide)_
- [ ] **FOXO4-DRI** — [`foxo4-dri.yaml`](./foxo4-dri.yaml) — _Senolytic peptide_
- [ ] **Thymalin** — [`thymalin.yaml`](./thymalin.yaml) — _Thymus-derived peptide bioregulator_
- [ ] **Vilon** — [`vilon.yaml`](./vilon.yaml) — _Thymus-derived dipeptide bioregulator_
- [ ] **NAD+** — [`nad-plus.yaml`](./nad-plus.yaml) — _Coenzyme central to cellular energy metabolism (not a peptide)_
- [ ] **Glutathione** — [`glutathione.yaml`](./glutathione.yaml) — _Tripeptide master antioxidant_

### Sexual Health
- [ ] **PT-141** — [`pt-141.yaml`](./pt-141.yaml) — _Melanocortin receptor agonist (Bremelanotide)_
- [ ] **Melanotan II** — [`melanotan-ii.yaml`](./melanotan-ii.yaml) — _Melanocortin agonist_
- [ ] **Kisspeptin-10** — [`kisspeptin-10.yaml`](./kisspeptin-10.yaml) — _Reproductive hormone regulator_
- [ ] **Gonadorelin** — [`gonadorelin.yaml`](./gonadorelin.yaml) — _GnRH analog_
- [ ] **HCG** — [`hcg.yaml`](./hcg.yaml) — _Human Chorionic Gonadotropin (not a peptide)_
- [ ] **HMG** — [`hmg.yaml`](./hmg.yaml) — _Human Menopausal Gonadotropin (not a peptide)_

### Immune & Inflammation
- [ ] **Thymosin Alpha-1** — [`thymosin-alpha-1.yaml`](./thymosin-alpha-1.yaml) — _Immune-modulating peptide_
- [ ] **LL-37** — [`ll-37.yaml`](./ll-37.yaml) — _Antimicrobial host-defense peptide_
- [ ] **Thymogen** — [`thymogen.yaml`](./thymogen.yaml) — _Immune-modulating dipeptide_

### Sleep & Relaxation
- [ ] **DSIP** — [`dsip.yaml`](./dsip.yaml) — _Delta sleep-inducing peptide_

### Skin & Anti-Aging
- [ ] **GHK-Cu** — [`ghk-cu.yaml`](./ghk-cu.yaml) — _Copper-binding tripeptide_
- [ ] **Melanotan I** — [`melanotan-i.yaml`](./melanotan-i.yaml) — _Melanocortin agonist (Afamelanotide)_
- [ ] **AHK-Cu** — [`ahk-cu.yaml`](./ahk-cu.yaml) — _Copper peptide variant of GHK-Cu_
- [ ] **SNAP-8** — [`snap-8.yaml`](./snap-8.yaml) — _Topical octapeptide_
- [ ] **Matrixyl** — [`matrixyl.yaml`](./matrixyl.yaml) — _Palmitoyl pentapeptide-4_
- [ ] **Botulinum Toxin** — [`botulinum-toxin.yaml`](./botulinum-toxin.yaml) — _Muscle-relaxing neurotoxin (not a peptide)_
- [ ] **Hyaluronic Acid** — [`hyaluronic-acid.yaml`](./hyaluronic-acid.yaml) — _Hydrating glycosaminoglycan (not a peptide)_

### Bone & Structural Health
- [ ] **Teriparatide** — [`teriparatide.yaml`](./teriparatide.yaml) — _PTH-derived peptide_

---

**Progress: 1 / 75 done.**
