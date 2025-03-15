# SilkCircuit - A Neon Dream for Home Assistant 🌃🦋

![GitHub release (latest by date)](https://img.shields.io/github/v/release/hyperb1iss/silkcircuit-theme)
![GitHub](https://img.shields.io/github/license/hyperb1iss/silkcircuit-theme)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

SilkCircuit is a vibrant, femme-forward theme for Home Assistant, glowing with neon elegance, sleek UI elements, and subtle digital charm. Immerse yourself in a high-tech, luminous dashboard experience that's as stylish as it is functional.

![SilkCircuit Theme Preview](https://raw.githubusercontent.com/hyperb1iss/silkcircuit-theme/main/screenshots/preview.png)

## 💅 Highlights

- **Radiant Neon Palette**: Hot pinks, lush purples, electric cyans, and vivid greens
- **Crystal Clear Contrast**: Bright, readable text on deep, luxurious backgrounds
- **Dreamy Gradients**: Soft, captivating gradients for depth and allure
- **Glowing Accents**: Interactive elements that pulse with neon energy
- **Elegant Cards**: Beautifully styled cards with digital-inspired details
- **Enhanced Sidebar**: Sleek navigation with custom neon touches
- **Intuitive Indicators**: Color-coded statuses for effortless readability
- **Gorgeous Dialogs**: Popups with a hazy backdrop and glowing borders

## 📸 Screenshots

...coming soon...

## 💿 Installation

### HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant
2. Navigate to HACS → Frontend
3. Click the "+" button
4. Search for "SilkCircuit"
5. Click Install
6. Restart Home Assistant

### Manual

1. Download `silkcircuit.yaml` from the `themes` folder
2. Create a `themes` folder in your Home Assistant config directory
3. Place the downloaded file inside
4. Add to your `configuration.yaml`:
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```
5. Restart Home Assistant

## 💫 Activate the Magic

1. Click your username in the sidebar
2. Under "Theme," select "SilkCircuit"
3. Bask in the neon glow!

### 🌙 Set as Default

To make SilkCircuit your default theme, add this to your `configuration.yaml`:

```yaml
frontend:
  themes: !include_dir_merge_named themes
  default_theme: silkcircuit
```

## 📌 Requirements

- Home Assistant 2023.3.0 or newer
- Card-mod integration (auto-installed via HACS)

## 🎨 Customization

SilkCircuit is crafted for easy personalization. Edit the `silkcircuit.yaml` file—every variable is clearly commented to guide your creativity.

## 📜 License

Licensed under the MIT License - see the LICENSE file for details.

<div align="center">

Created by [Stefanie Jane 🌠](https://github.com/hyperb1iss)

If you like this, star my repo and [buy me a Monster Ultra Violet!](https://ko-fi.com/hyperb1iss) ⚡️

</div>
