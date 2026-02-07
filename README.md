# procedural-groom-density-mask
<I>Research Project: Procedural Groom Density Mask Generation by Region in Maya</I>

---



**Overview**

This project explores a procedural approach to generating base hair density masks for XGen grooming in Maya, reducing repetitive manual mask painting through rule-based scripting.

---

**Pipeline Summary**

- Maya Python script extracts UV-aligned region data
- External Python script generates procedural base density masks
- Outputs are saved as UDIM-aligned texture maps for XGen workflows

---

**Repository Structure**

- 1_maya_cmd_FIN.py : Maya Python script for extracting UV and region data
- 2_horse_uv_faces_triangulated.json : Exported UV/face region data
- 3_create_densitymaskimages_rampnoiseblur.py : External Python script for mask generation
- horse_density_*.png : Generated base density masks and results

---

**Notes**

This repository is intended for code review and pipeline understanding.
Direct execution requires the original Maya scene file and environment setup.

---

**Author**

Hanyu Lee — VFX / Technical Art
