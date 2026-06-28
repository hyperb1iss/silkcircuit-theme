# SilkCircuit — A Neon Dream for Home Assistant 🌃🦋

<div align="center">

[![](https://img.shields.io/github/v/release/hyperb1iss/silkcircuit-theme?style=for-the-badge&logo=github&logoColor=white&labelColor=12101a&color=e135ff)](https://github.com/hyperb1iss/silkcircuit-theme/releases)
[![](https://img.shields.io/github/license/hyperb1iss/silkcircuit-theme?style=for-the-badge&logo=law&logoColor=white&labelColor=12101a&color=80ffea)](https://github.com/hyperb1iss/silkcircuit-theme/blob/main/LICENSE)
[![](https://img.shields.io/badge/HACS-Default-50fa7b?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white&labelColor=12101a)](https://github.com/hacs/integration)

<img src="https://raw.githubusercontent.com/hyperb1iss/silkcircuit-theme/main/images/silkcircuit-theme.png" alt="SilkCircuit Theme Preview" width="800">

**Electric purple, neon cyan, and a signature pink glow on deep, near-black backgrounds.**

![](https://placehold.co/15x15/e135ff/e135ff.png) `#e135ff` &nbsp;
![](https://placehold.co/15x15/ff6ac1/ff6ac1.png) `#ff6ac1` &nbsp;
![](https://placehold.co/15x15/ff00ff/ff00ff.png) `#ff00ff` &nbsp;
![](https://placehold.co/15x15/80ffea/80ffea.png) `#80ffea` &nbsp;
![](https://placehold.co/15x15/50fa7b/50fa7b.png) `#50fa7b` &nbsp;
![](https://placehold.co/15x15/f1fa8c/f1fa8c.png) `#f1fa8c` &nbsp;
![](https://placehold.co/15x15/ff6363/ff6363.png) `#ff6363`

</div>

SilkCircuit is the femme-forward face of the [SilkCircuit design language](https://github.com/hyperb1iss/silkcircuit-nvim), brought to Home Assistant — high-tech and luminous, as stylish as it is readable.

## 🎨 Variants

Six themes ship in one file. Pick any of them from your profile — they all appear in the theme picker.

| Variant | Signature | Vibe | Surface |
| --- | --- | --- | --- |
| **SilkCircuit** | ![](https://placehold.co/15x15/e135ff/e135ff.png) `#e135ff` | The flagship neon experience | ![](https://placehold.co/15x15/12101a/12101a.png) `#12101a` |
| **SilkCircuit Vibrant** | ![](https://placehold.co/15x15/ff00ff/ff00ff.png) `#ff00ff` | Punchier, magenta-forward | ![](https://placehold.co/15x15/0f0c1a/0f0c1a.png) `#0f0c1a` |
| **SilkCircuit Soft** | ![](https://placehold.co/15x15/e892ff/e892ff.png) `#e892ff` | Gentle pastels for long sessions | ![](https://placehold.co/15x15/1a1626/1a1626.png) `#1a1626` |
| **SilkCircuit Glow** | ![](https://placehold.co/15x15/ff00ff/ff00ff.png) `#ff00ff` | Ultra-dark, pure neon, max contrast | ![](https://placehold.co/15x15/0a0816/0a0816.png) `#0a0816` |
| **SilkCircuit Dawn** | ![](https://placehold.co/15x15/7e2bd5/7e2bd5.png) `#7e2bd5` | Light theme for daytime | ![](https://placehold.co/15x15/faf8ff/faf8ff.png) `#faf8ff` |
| **SilkCircuit Auto** | 🌗 | Follows system light/dark — Dawn by day, Neon by night | adaptive |

All variants share the same semantic palette: **purple** for primary actions, **cyan** for interaction, **green** for "on", **red** for "off", **yellow** for attention, and a **pink** glow on cards and dialogs.

## 💅 Highlights

- **Real SilkCircuit palette** — the canonical neon colors, not an approximation
- **Five hand-tuned variants + an auto light/dark theme** for every room and time of day
- **Crystal-clear contrast** — bright, readable text on luxurious backgrounds
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
