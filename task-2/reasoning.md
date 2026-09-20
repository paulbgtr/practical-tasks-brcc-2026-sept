# Task 2

## 1. What is the total production capacity of the generators in the model?

I found three `SynchronousMachine` objects (NL-G1, NL-G2, NL-G3), each referencing a `GeneratingUnit`. `SynchronousMachine.ratedS` represents apparent power (S) while `GeneratingUnit.maxOperatingP` represents active power (P) - the actual maximum power the unit can deliver to the grid. Since "production capacity" refers to real power output rather than the machine's apparent power rating, I used maxOperatingP:

Gen-12923 (NL-G1): 1000 MW
Gen-12908 (NL-G3): 250 MW
Gen-12910 (NL-G2): 250 MW

Total production capacity: 1500 MW

Note: the term "capacity" is somewhat ambiguous - it could refer to the maximum operating limit (`maxOperatingP`, used above) or to the nominal/nameplate rating (`nominalP`). For reference, summing nominalP instead gives 990 + 225 + 225 = 1440 MW. I used `maxOperatingP` since "capacity" typically denotes the upper technical limit rather than the typical operating point.

The generator models used for the calculations:

```xml
<cim:GeneratingUnit rdf:ID="_b850063d-eae7-4675-bc98-4642d3076783">
  <cim:IdentifiedObject.name>Gen-12908</cim:IdentifiedObject.name>
  <cim:IdentifiedObject.description>Machine</cim:IdentifiedObject.description>
  <cim:Equipment.aggregate>false</cim:Equipment.aggregate>
  <cim:Equipment.EquipmentContainer rdf:resource="#_c49942d6-8b01-4b01-b5e8-f1180f84906c"/>
  <cim:GeneratingUnit.genControlSource
    rdf:resource="http://iec.ch/TC57/CIM100#GeneratorControlSource.offAGC"/>
  <cim:GeneratingUnit.maxOperatingP>250</cim:GeneratingUnit.maxOperatingP>
  <cim:GeneratingUnit.minOperatingP>130</cim:GeneratingUnit.minOperatingP>
  <cim:GeneratingUnit.nominalP>225</cim:GeneratingUnit.nominalP>
  <cim:IdentifiedObject.mRID>b850063d-eae7-4675-bc98-4642d3076783</cim:IdentifiedObject.mRID>
</cim:GeneratingUnit>
```

```xml
<cim:GeneratingUnit rdf:ID="_049438a6-780a-44fe-a788-ebe385d98e25">
    <cim:IdentifiedObject.name>Gen-12923</cim:IdentifiedObject.name>
    <cim:IdentifiedObject.description>Machine</cim:IdentifiedObject.description>
    <cim:Equipment.aggregate>false</cim:Equipment.aggregate>
    <cim:Equipment.EquipmentContainer rdf:resource="#_c49942d6-8b01-4b01-b5e8-f1180f84906c"/>
    <cim:GeneratingUnit.genControlSource
        rdf:resource="http://iec.ch/TC57/CIM100#GeneratorControlSource.offAGC"/>
    <cim:GeneratingUnit.maxOperatingP>1000</cim:GeneratingUnit.maxOperatingP>
    <cim:GeneratingUnit.minOperatingP>300</cim:GeneratingUnit.minOperatingP>
    <cim:GeneratingUnit.nominalP>990</cim:GeneratingUnit.nominalP>
    <cim:IdentifiedObject.mRID>049438a6-780a-44fe-a788-ebe385d98e25</cim:IdentifiedObject.mRID>
</cim:GeneratingUnit>
```

```xml
  <cim:GeneratingUnit rdf:ID="_ca80ee09-3bed-4884-bc28-6dc89d067289">
    <cim:IdentifiedObject.name>Gen-12910</cim:IdentifiedObject.name>
    <cim:IdentifiedObject.description>Machine</cim:IdentifiedObject.description>
    <cim:Equipment.aggregate>false</cim:Equipment.aggregate>
    <cim:Equipment.EquipmentContainer rdf:resource="#_c49942d6-8b01-4b01-b5e8-f1180f84906c"/>
    <cim:GeneratingUnit.genControlSource
      rdf:resource="http://iec.ch/TC57/CIM100#GeneratorControlSource.offAGC"/>
    <cim:GeneratingUnit.maxOperatingP>250</cim:GeneratingUnit.maxOperatingP>
    <cim:GeneratingUnit.minOperatingP>130</cim:GeneratingUnit.minOperatingP>
    <cim:GeneratingUnit.nominalP>225</cim:GeneratingUnit.nominalP>
    <cim:IdentifiedObject.mRID>ca80ee09-3bed-4884-bc28-6dc89d067289</cim:IdentifiedObject.mRID>
  </cim:GeneratingUnit>
```

## 2. What are the nominal voltages of the windings of the transformer `NL_TR2_2` (ID: `_2184f365-8cd5-4b5d-8a28-9d68603bb6a4`)?

The transformer `NL_TR2_2` (`_2184f365-...`) has 2 real windings. A literal search for `PowerTransformerEnd` objects referencing this transformer returns 4 results, but 2 of them (named "NL_TR2_3" and "NL_TR2_4") are corrupted duplicates, not genuine additional windings:

- They share the exact same `rdf:ID` (`_0dbed103-...`) as the legitimate End 1 of NL_TR2_2, which causes `rdflib` to reject the file (RDF requires unique IDs).
- They reference the same `Terminal` (`_421c7930-...`) as End 1 which is physically impossible, since a single terminal cannot belong to three different transformer windings simultaneously.
- Their electrical parameters (r, x, g, b) are identical to End 1's, down to 7 significant figures.
- The file elsewhere contains a real `PowerTransformer` named `NL_TR2_3` (`_80016742-...`) with its own distinct ID, terminal, and slightly different parameters confirming that the "NL_TR2_3" duplicate here is not that real transformer, just a corrupted copy-paste artifact.

I treated this as a modeling bug (likely a copy-paste error during file generation, addressed further in Question 5) and excluded these duplicates from the calculation. The actual windings of NL_TR2_2 are:

- End 1 (HV): ratedU = 220 kV
- End 2 (LV): ratedU = 15.75 kV

## 3. What is the permanently allowed limit for line segment `NL-Line_5` (ID: `_e8acf6b6-99cb-45ad-b8dc-16c7866a4ddc`) and temporarily allowed? What is the difference between those limits?

For line segment `NL-Line_5` (`_e8acf6b6-...`), the `OperationalLimitSet`/`CurrentLimit` objects report:

- PATL (Permanently Admissible Transmission Limit): 1876 A
- TATL (Temporarily Admissible Transmission Limit): 500 A
- Difference: 1876 − 500 = 1376 A

These values are identical at both terminals (Port 1 and Port 2), which is expected for a single line segment.

By definition, PATL is the current a conductor can carry continuously, while TATL is the current allowed only for a limited duration (e.g. during contingencies), and is normally higher than PATL, short-term thermal inertia allows temporary overloading beyond the continuous rating.

Here, TATL (500 A) is lower than PATL (1876 A), which is physically inconsistent: it would imply the line is more restricted during emergency conditions than during normal operation, this is the opposite of the intended purpose of a temporary limit.

This is flagged as a modeling error in Question 5: PATL and TATL appear to be either swapped or one of them was populated with a placeholder value (500 A) instead of the correct calculated limit.

## 4. Which generator is set as slack in the model? Why does the model need a slack node?

NL-G1 is the most likely slack generator, though this file doesn't explicitly label one.

NL-G1 is the only generator with a voltage-regulating control (RegulatingControl, mode = voltage) instead of a fixed power output this is the kind of behavior a slack node needs. It's also the biggest generator (1000 of 1500 MW total), which makes sense for a slack node since it needs room to absorb whatever imbalance shows up.

One caveat: voltage regulation alone doesn't prove it's the slack node. There's a shunt compensator (NL-S1) elsewhere in the file with the same kind of voltage control, so this mechanism isn't unique to slack generators. Based on what's actually in this file, NL-G1 is the best-supported guess, but I can't confirm it 100%.

Why a slack node is needed: in a power flow calculation, you need one reference point for two things: the voltage angle (only the difference between two points' angles actually matters, so one has to be fixed at 0 degrees as a baseline), and the overall power balance (line losses aren't known ahead of time since they depend on the final result, so one generator's output is left unfixed and just absorbs whatever's left over once everything else balances out).

## 5. Find mistakes in the model (semantic, power system related, and logical errors are all present).

### 1. Duplicate ID across three transformer windings

Three different `PowerTransformerEnd` objects (named NL_TR2_2, NL_TR2_3, NL_TR2_4) all share the same `rdf:ID` (`_0dbed103-...`). This breaks RDF's uniqueness rule, and rdflib refuses to even parse the file because of it. On top of that, all three reference the exact same `Terminal` and have identical electrical parameters (r, x, g, b) down to 7 significant figures - physically impossible for three different transformers. The real NL_TR2_3 exists elsewhere in the file with its own distinct ID, terminal, and slightly different parameters, confirming this is a copy-paste error, not three real windings.

### 2. TATL lower than PATL (inverted on every line)

On every checked line (NL-Line_1 through NL-Line_5, NL-Line_4), the temporary limit (TATL) is lower than the permanent limit (PATL) - e.g. NL-Line_5 has PATL = 1876 A but TATL = 500 A. This is backwards: TATL should always be higher, since a line can handle a short-term overload that it couldn't sustain continuously. The fact that TATL = 500 A on nearly every line, regardless of the line's actual PATL, suggests it was left as a placeholder value rather than calculated per line.

### 3. Broken reference: TATL's OperationalLimitType ID doesn't match its own mRID

```xml
<cim:OperationalLimitType rdf:ID="_bf2a4896-2e92-465b-b5f9-b033993a318">
  ...
  <cim:IdentifiedObject.mRID>bf2a4896-2e92-465b-b5f9-b033993a31c8</cim:IdentifiedObject.mRID>
```

The `rdf:ID` ends in `...a318`, but the `mRID` (and every CurrentLimit in the file that points to this TATL type) references `...a31c8`. These are two different strings, every TATL limit in the file technically points to an object that doesn't exist under that ID.

### 4. Missing `ratedU` on generator NL-G3

NL-G1 and NL-G2 both specify `RotatingMachine.ratedU = 15.75`, but NL-G3 has no `ratedU` at all, despite being the same type of machine with otherwise similar parameters.

### 5. Broken resource reference on NL-G1's GeneratingUnit link

```xml
<cim:RotatingMachine.GeneratingUnit rdf:resource="_049438a6-780a-44fe-a788-ebe385d98e25"/>
```

Missing the `#` before the ID. Every other object in the file correctly uses `rdf:resource="#_id"` to link to a local object; without the `#`, this is interpreted as an external URI rather than a reference to the GeneratingUnit in the same document - the link is effectively broken.

### 6. Mislabeled VoltageLevel

A `VoltageLevel` (`_b7998ae6-0cc6-4dfe-8fec-0b549b07b6c3`) object is named "900.0" with `highVoltageLimit = 999` / `lowVoltageLimit = 600`, but its linked BaseVoltage (`_597e44dc-...`) is the same one used by lines and transformers rated at 400 kV elsewhere in the file. The name and limits don't match the actual voltage class.
