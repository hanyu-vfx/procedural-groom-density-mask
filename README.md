# procedural-groom-density-mask
Procedural groom base density mask generation using region-based rules in Maya.

Procedural Groom Density Mask Generation (Maya)

**Overview**

This project explores a procedural approach to generating base groom density masks for XGen in Autodesk Maya.
Instead of manually painting density maps, the system generates UV-aligned base density masks using region-based rules and programmatic logic, providing a clean and reusable foundation for further grooming refinement.
The project was developed as part of a creative computing / technical exploration, focusing on workflow scalability and structural control rather than purely visual outcomes.

---
**Motivation**

Traditional XGen density mask workflows rely heavily on manual painting, which:
Is time-consuming and repetitive
Becomes error-prone on complex meshes
Does not scale well across multiple regions or UDIMs

This project investigates whether hair density can be treated as a continuous, computable value, allowing density control to be handled procedurally rather than manually.


---

**Key Features**

Procedural base density mask generation
UV-aligned output matching the original mesh layout
Multi-UDIM–aware workflow (e.g. UDIM 1001 / 1002)
Clean base masks suitable for further gradient or rule-based modulation
Designed to integrate with XGen groom workflows in Maya

---

**Workflow Summary**

1. Input mesh with existing UV layout
2. Region-based and UV-aware computation of base density values
3. Generation of intermediate UV-aligned density maps
4. Export of final base density masks as image files (PNG)
5. Masks applied and tested within Maya XGen

---

**Technical Notes**
The system is designed to run inside a Maya environment
Some post processing steps rely on external Python scripts
Full execution requires:
Autodesk Maya
Python scripting environment
A compatible .mb scene file
> This repository focuses on demonstrating the logic, structure, and workflow design rather than providing a one-click standalone tool.

---

**Repository Contents**

/scripts – Python scripts used for procedural density generation

/examples – Example outputs and reference images

/docs – Visual explanations and workflow breakdowns

---

**Author**
Hanyu Lee
VFX / Technical Art
