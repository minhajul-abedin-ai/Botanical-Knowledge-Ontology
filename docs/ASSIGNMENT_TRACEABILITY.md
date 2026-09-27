# Assignment traceability

This repository is a **portfolio reconstruction**, not the original submitted Protégé project.
The original ontology file was no longer available, so the implementation was rebuilt from the concepts, examples and reasoning scenarios described in the academic assignment.

## Directly supported by the assignment

The reconstruction preserves the following elements described in the report:

- Protégé-based ontology engineering following the KADO-oriented lifecycle.
- A core `Vegetable` hierarchy with `RootVegetable`, `LeafyVegetable`, `LegumeVegetable` and `FruitVegetable`.
- A parallel `PlantPart` hierarchy containing root, stem, leaf and seed structures, including `TapRoot`, `FibrousRoot`, `SimpleLeaf`, `CompoundLeaf`, `MonocotSeed` and `DicotSeed`.
- Disjointness constraints, especially Root vs Leaf vegetable categories and Monocot vs Dicot seeds.
- Mereological relationships using `hasPart` / `isPartOf`, with `hasPart` treated as transitive.
- Object properties including `hasGrowthHabit`, `hasFlower`, `hasPod` and `usedInCuisine`.
- Data properties including `proteinPer100g`, `carbPer100g`, `fatPer100g`, `hasVitaminA`, `hasVitaminC`, `hasVitaminK`, `growthTimeDays`, `hasOrigin`, `hasColor` and `hasTaste`.
- Individuals such as `Carrot_ind`, `Spinach_ind` and `Tomato_ind`.
- Explicit carrot facts: orange colour, 70-day growth time and Vitamin A = true.
- Explicit phenology examples: Radish = 25 days and Pumpkin = 90 days.
- Reasoning scenarios around biofortification, fast-growing crops, crop succession and neuro-symbolic grounding.
- Use of OWL 2 DL and Pellet-style reasoning in Protégé.

## Source-derived inferences

The report states that certain queries return specific individuals but does not provide every underlying numeric assertion. To avoid inventing exact values, the reconstruction models those results as semantic classes:

- `FastGrowingCrop`: assigned to `Bean_ind`, `Beetroot_ind` and `Spinach_ind` because the assignment states that relevant under-60-day queries return those examples.
- `HighProteinCrop`: assigned to `Spinach_ind` because the neuro-symbolic example states that a >2g protein and <60-day query retrieves Spinach.
- `MaturesUnder120Days`: assigned to `Carrot_ind` and `SweetPotato_ind` to preserve the biofortification scenario without inventing an exact Sweet Potato growth duration.

The `data/source_supported_facts.csv` file labels each fact as `assignment-explicit` or `assignment-inferred`.

## Portfolio additions

The following are engineering additions made to turn the coursework into a reproducible GitHub project. They were **not claimed to be present in the original submission**:

- Reproducible Python ontology builder using RDFLib.
- RDF/XML and Turtle exports.
- SPARQL query files.
- Automated structural validation.
- Pytest test suite and GitHub Actions workflow.
- Programmatically generated hierarchy and architecture diagrams.
- Repository documentation, license, citation metadata and upload guide.

## Deliberate handling of one source inconsistency

The assignment text gives an example `Carrot_ind hasTuber tuber1`, while elsewhere modelling carrot as a root/taproot vegetable. The reconstruction does **not silently reproduce that biologically awkward assertion**. Instead, `Carrot_ind` is linked to `CarrotTapRoot` through `hasPart`, and this design choice is documented here.
