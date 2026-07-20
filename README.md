# Maryam's PhD Thesis

This repository contains the LaTeX source code and compiled PDF for a PhD thesis focused on **2.5D Terrain-Aware Path Planning for Autonomous Ground Vehicles in Unstructured Agricultural Environments**.

## Overview

The thesis explores advanced navigation architectures for heavy agricultural machinery operating in challenging, off-road terrains. It introduces a modified A* graph-search algorithm that directly integrates three-dimensional step distances (3DSD) and localized slope magnitudes (SM) to ensure safe, energy-efficient routing, coupled with B-spline trajectory refinement.

## Repository Structure

- `UMP template.tex`: The main LaTeX driver file that includes all chapters and frontmatter.
- `Frontmatter/`: Contains the title page, declarations, acknowledgements, abstract, and table of contents.
- `Chap1/` - `Chap5/`: Individual chapter source files containing the core content of the thesis.
- `Appendix/`: Supplementary material and appendices.
- `figures/`: Images, charts, and diagrams used throughout the chapters.
- `rujukan.bib`: The central bibliography file containing all formatted references used in the thesis.
- `REFERENCE CHECK/`: Contains automated reports verifying the bibliography entries and citation contexts.
- `format_tex.py`: A utility Python script used to format and wrap `.tex` files for improved readability.
- `UMP template.pdf`: The latest successfully compiled output of the thesis.

## Compilation

To compile this thesis locally, it is highly recommended to use [Tectonic](https://tectonic-typesetting.github.io/), a modernized, complete, self-contained TeX/LaTeX engine. 

Run the following command from the root directory of this repository:

```bash
tectonic "UMP template.tex"
```

Tectonic will automatically handle all multiple compilation passes (including `bibtex` for the references) and output the final `UMP template.pdf`.

## License & Usage

All content in this repository is proprietary and belongs to the author. Do not distribute or use without permission.
