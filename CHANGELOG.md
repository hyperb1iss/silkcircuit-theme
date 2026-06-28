# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-06-28

First tagged release — the electric, femme-forward face of the
[SilkCircuit design language](https://github.com/hyperb1iss/silkcircuit-nvim),
brought to Home Assistant.

### Added

- **Six themes in one file**: SilkCircuit (Neon flagship), Vibrant, Soft, Glow,
  Dawn (light), and Auto, which follows the system light/dark setting — Dawn by
  day, Neon by night.
- **Canonical SilkCircuit palette** across every variant, sourced from
  `silkcircuit-nvim`: electric purple `#e135ff`, neon cyan `#80ffea`, and the
  signature pink glow on deep, near-black backgrounds.
- **Comprehensive Home Assistant coverage**: cards, sidebar, controls, MDC
  inputs and selects, dialogs, badges, climate, energy, and more.
- **Card-mod enhancements**: sidebar gradient, glow-on-hover cards, and hazy
  dialog backdrops.
- **Generator** (`scripts/build_theme.py`) that expands one shared body across
  all variants and self-checks that every `var(--color-*)` token is defined.

[1.0.0]: https://github.com/hyperb1iss/silkcircuit-theme/releases/tag/v1.0.0
