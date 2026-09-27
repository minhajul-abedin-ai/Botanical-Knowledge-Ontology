# Ontology design

## Goal

Represent botanical, agricultural and nutritional knowledge in one semantic model so that queries can combine taxonomy, morphology, nutrition and growth information.

## Core class hierarchy

```text
BotanicalEntity
├── Plant
├── Vegetable
│   ├── RootVegetable
│   ├── LeafyVegetable
│   ├── LegumeVegetable
│   ├── FruitVegetable
│   ├── BulbVegetable
│   └── CruciferousVegetable
├── PlantPart
│   ├── Root
│   │   ├── TapRoot
│   │   └── FibrousRoot
│   ├── Stem
│   ├── Leaf
│   │   ├── SimpleLeaf
│   │   └── CompoundLeaf
│   ├── Seed
│   │   ├── MonocotSeed
│   │   └── DicotSeed
│   ├── Fruit
│   └── Tuber
├── Nutrient
│   ├── Macronutrient
│   │   ├── Protein
│   │   ├── Carbohydrate
│   │   └── Fat
│   └── Micronutrient
│       ├── VitaminA
│       ├── VitaminC
│       └── VitaminK
├── GrowthHabit
└── Cuisine
```

`BulbVegetable` and `CruciferousVegetable` are retained because the assignment discusses bulb substitution and cruciferous/legume-style taxonomies, but their use is intentionally light because detailed source assertions were not supplied.

## Object properties

| Property | Purpose |
|---|---|
| `hasPart` | Whole-to-part relation; modelled as transitive |
| `isPartOf` | Inverse of `hasPart` |
| `hasGrowthHabit` | Links crop to a plant form/growth habit |
| `hasFlower` | Links plant/crop to a flower entity |
| `hasPod` | Links legumes to pod structures |
| `usedInCuisine` | Links a vegetable to a culinary context |

## Data properties

| Property | Range |
|---|---|
| `proteinPer100g` | decimal |
| `carbPer100g` | decimal |
| `fatPer100g` | decimal |
| `caloriesPer100g` | integer |
| `hasVitaminA` | boolean |
| `hasVitaminC` | boolean |
| `hasVitaminK` | boolean |
| `growthTimeDays` | integer |
| `hasOrigin` | string |
| `hasColor` | string |
| `hasTaste` | string |

## Reasoning-oriented helper classes

To reproduce assignment-described query outcomes without inventing missing exact measurements, the portfolio version includes:

- `FastGrowingCrop`
- `HighProteinCrop`
- `MaturesUnder120Days`
- `VitaminARichCrop`

These helper classes are documented as reconstruction aids, not as hidden claims about the original ontology.

## Logical constraints

- `RootVegetable` disjoint with `LeafyVegetable`.
- `MonocotSeed` disjoint with `DicotSeed`.
- `hasPart` is transitive.
- `isPartOf` is inverse of `hasPart`.

## Tooling

The original report describes OWL 2 DL and Pellet reasoning in Protégé. This repository provides standards-compatible OWL/RDF exports that can be opened in Protégé. The Python utilities use RDFLib for reproducible loading, querying and structural validation; full OWL DL classification should still be performed in Protégé with a DL reasoner such as Pellet/HermiT.
