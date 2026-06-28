# SilkCircuit — A Neon Dream for Home Assistant 🌃🦋

<div align="center">

[![](https://img.shields.io/github/v/release/hyperb1iss/silkcircuit-theme?style=for-the-badge&logo=github&logoColor=white&labelColor=12101a&color=e135ff)](https://github.com/hyperb1iss/silkcircuit-theme/releases)
[![](https://img.shields.io/github/license/hyperb1iss/silkcircuit-theme?style=for-the-badge&logo=law&logoColor=white&labelColor=12101a&color=80ffea)](https://github.com/hyperb1iss/silkcircuit-theme/blob/main/LICENSE)
[![](https://img.shields.io/badge/HACS-Default-50fa7b?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white&labelColor=12101a)](https://github.com/hacs/integration)

<img src="https://raw.githubusercontent.com/hyperb1iss/silkcircuit-theme/main/images/silkcircuit-theme.png" alt="SilkCircuit Theme Preview" width="800">

</div>

SilkCircuit is the electric, femme-forward face of the [SilkCircuit design language](https://github.com/hyperb1iss/silkcircuit-nvim), brought to Home Assistant. Electric purple, neon cyan, and a signature pink glow on deep, near-black backgrounds — high-tech and luminous, as stylish as it is readable.

## 🎨 Variants

Six themes ship in one file. Pick any of them from your profile — they all show up in the theme picker.

| Theme | Vibe | Background | Primary |
| --- | --- | --- | --- |
| **SilkCircuit** | The flagship neon experience | `#12101a` | electric purple `#e135ff` |
| **SilkCircuit Vibrant** | Punchier, magenta-forward | `#0f0c1a` | magenta `#ff00ff` |
| **SilkCircuit Soft** | Gentler pastels, easy for long sessions | `#1a1626` | soft purple `#e892ff` |
| **SilkCircuit Glow** | Ultra-dark with pure neon — maximum contrast | `#0a0816` | pure magenta `#ff00ff` |
| **SilkCircuit Dawn** | Light theme for daytime | `#faf8ff` | deep purple `#7e2bd5` |
| **SilkCircuit Auto** | Follows your system light/dark — Dawn by day, Neon by night | adaptive | adaptive |

All variants share the same semantic palette: purple for primary actions, cyan for interaction, green for "on", red for "off", yellow for attention, and a pink glow on cards and dialogs.

## 💅 Highlights

- **Real SilkCircuit palette** — the canonical neon colors, not an approximation
- **Five hand-tuned variants + an auto light/dark theme** for every room and time of day
- **Crystal-clear contrast** — bright, readable text on luxurious backgrounds (WCAG-minded)
- **Glowing accents** — cards, dialogs, and controls that pulse with neon energy
- **Comprehensive coverage** — sliders, switches, MDC inputs, climate, energy, badges, and more
- **Card-mod enhancements** — sidebar gradient, glow-on-hover cards, hazy dialog backdrops

## 💿 Installation

### HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant
2. Navigate to **HACS → Frontend**
3. Click the **+** button and search for **SilkCircuit**
4. Click **Install**, then restart Home Assistant

### Manual

1. Download `silkcircuit.yaml` from the `themes` folder
2. Place it in a `themes` folder in your Home Assistant config directory
3. Add to your `configuration.yaml` (if not already present):
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```
4. Restart Home Assistant

## 💫 Activate the Magic

1. Click your username in the sidebar
2. Under **Theme**, pick any **SilkCircuit** variant
3. Bask in the neon glow

### 🌙 Set as Default

```yaml
frontend:
  themes: !include_dir_merge_named themes
  default_theme: SilkCircuit
```

The **SilkCircuit Auto** variant respects Home Assistant's light/dark mode automatically — set it as your default and it switches between Dawn and Neon with the system.

## 🛠️ Development

The theme file is **generated** — every visual rule lives once in the build script and is expanded across all variants, so a variant is just its palette. Don't hand-edit `themes/silkcircuit.yaml`; edit the script and regenerate:

```bash
python3 scripts/build_theme.py   # or: uv run scripts/build_theme.py
```

Palettes are lifted from the source of truth in [`silkcircuit-nvim`](https://github.com/hyperb1iss/silkcircuit-nvim). To tweak a color or add a variant, edit `PALETTES` in `scripts/build_theme.py`. The script self-checks that every `var(--color-*)` it references is defined for every variant.

## 📌 Requirements

- Home Assistant 2023.3.0 or newer
- Card-mod (auto-installed via HACS)

## 📜 License

Licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

<div align="center">

Created by [Stefanie Jane 🌠](https://github.com/hyperb1iss)

If you like this, star the repo and [buy me a Monster Ultra Violet!](https://ko-fi.com/hyperb1iss) ⚡️

</div>
