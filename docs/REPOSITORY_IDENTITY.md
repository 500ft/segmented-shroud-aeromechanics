# Repository identity and reading conventions

Updated September 10, 2026. The project is now **Segmented Shroud Aeromechanics**, at
[`500ft/segmented-shroud-aeromechanics`](https://github.com/500ft/segmented-shroud-aeromechanics).
Its previous repository name was `Segmented-Shroud-Yield`; this is a rename of the same
repository, not a new project or release.

## What the rename changes

The public name, GitHub description, README navigation and active repository
links use the new identity. Historical commits, paper titles, preregistrations,
data, release artifacts, measurements and approval records retain their original
meaning. Legacy package/module names remain valid; repository branding does not
rename an import or command-line API.

To update an existing clone without moving its files:

```sh
git remote set-url origin https://github.com/500ft/segmented-shroud-aeromechanics.git
git remote -v
```

GitHub redirects the old repository location. Do not create a replacement under
the old name: that would remove the redirect. See
[GitHub's rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).
Historical source URLs and immutable evidence records are intentionally not
mass-edited just to remove the former name.

## Reading routes

The [README](../README.md) is the project overview.
[Start here](START_HERE.md) offers short paths for readers, technical reviewers
and contributors. Detailed claims remain in their source documents; an overview
does not replace the authoritative protocol or task ledger.

## Visual provenance

The README leads with [`media/project-overview.svg`](media/project-overview.svg),
an editable diagram of the three remaining steps in the [roadmap](../ROADMAP.md).
It contains no results, because none exist yet. Each step has a text label, so
the meaning doesn't depend on colour, and the SVG has a title and description
for screen readers. Update it in the same PR as any change to the roadmap's
steps. Once a baseline solution exists, a plot of it should replace the
diagram as the lead image.

## Keeping navigation reproducible

From the repository root:

```sh
python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics
python tools/test_presentation.py
```

CI runs these checks alongside the existing project gates. They check the README,
reading guide, identity note, contribution guide and figure guide: local paths,
anchors, canonical title/CI badge, image alternative text and SVG accessibility.
Four offline cases confirm valid input passes while missing links, wrong anchors
and identity/accessibility errors fail. This is a bounded presentation checker,
not an exhaustive Markdown parser, external-link crawler or scientific validator.

## Presentation references

The organization is informed by these examples, reviewed September 10, 2026:

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template):
  a readable introduction, navigation and actionable getting-started sections.
- [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science):
  distinct paths for data, analysis and reports.
- [gym-pybullet-drones](https://github.com/learnsyslab/gym-pybullet-drones):
  reproducible use, environment boundaries and source/citation entry points.

The text and overview diagram are project-specific; no template screenshot,
branding, claim of adoption or unrelated technology badge is borrowed.
These presentation changes do not change this repository's existing licensing,
grant permission for hardware tests, or establish a publication/validation verdict.
