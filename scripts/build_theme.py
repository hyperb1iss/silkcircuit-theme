#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Generate themes/silkcircuit.yaml — real SilkCircuit for Home Assistant.

Every visual rule lives once in ``BODY`` and resolves through ``var(--color-*)``
CSS variables, so a variant is nothing but its palette block. Home Assistant's
YAML loader has no merge keys, so we expand that one body across every variant
here instead of leaning on anchors.

Palettes are the canonical SilkCircuit colors, lifted from the source of truth
in ``silkcircuit-nvim`` (lua/silkcircuit/variants.lua): Neon, Vibrant, Soft,
Glow and Dawn. The flagship is purple-primary (#e135ff) with the signature
pink glow; "SilkCircuit Auto" follows the system light/dark setting, pairing
Dawn by day with Neon by night.

Run:  python3 scripts/build_theme.py   (or: uv run scripts/build_theme.py)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "themes" / "silkcircuit.yaml"

# Order palette keys are emitted in. Every key gets a `--color-<key>` plus a
# `--color-<key>-rgb` triplet so rgba(var(--color-<key>-rgb), a) always works.
TOKEN_ORDER = [
    "primary",
    "primary-light",
    "primary-dark",
    "pink",
    "pink-light",
    "magenta",
    "cyan",
    "cyan-light",
    "green",
    "green-light",
    "yellow",
    "orange",
    "coral",
    "teal",
    "red",
    "text",
    "text-muted",
    "text-disabled",
    "text-on-accent",
    "muted",
    "muted-dark",
    "white",
    "off-white",
    "bg",
    "bg-card",
    "bg-elevated",
    "bg-sidebar",
    "divider",
    "glow",
]

# Canonical SilkCircuit palettes. Core hues match silkcircuit-nvim; backgrounds
# are laddered for HA's card/sidebar/elevated surfaces and text roles invert for
# the light (Dawn) variant.
PALETTES: dict[str, dict[str, str]] = {
    "neon": {
        "primary": "#e135ff",
        "primary-light": "#f2a6ff",
        "primary-dark": "#b06cff",
        "pink": "#ff6ac1",
        "pink-light": "#ff99dd",
        "magenta": "#ff00ff",
        "cyan": "#80ffea",
        "cyan-light": "#b3fff2",
        "green": "#50fa7b",
        "green-light": "#7dffa0",
        "yellow": "#f1fa8c",
        "orange": "#ffb86c",
        "coral": "#ff6ac1",
        "teal": "#4fffb0",
        "red": "#ff6363",
        "text": "#f8f8f2",
        "text-muted": "#c9c2e6",
        "text-disabled": "#8c86a8",
        "text-on-accent": "#12101a",
        "muted": "#8c8cb0",
        "muted-dark": "#5a5a7a",
        "white": "#ffffff",
        "off-white": "#f0f0ff",
        "bg": "#12101a",
        "bg-card": "#1a162a",
        "bg-elevated": "#221c34",
        "bg-sidebar": "#0a0812",
        "divider": "#332b4d",
        "glow": "#ff6ac1",
    },
    "vibrant": {
        "primary": "#ff00ff",
        "primary-light": "#ff66ff",
        "primary-dark": "#c200c2",
        "pink": "#ff00cc",
        "pink-light": "#ff66dd",
        "magenta": "#ff00ff",
        "cyan": "#00ffcc",
        "cyan-light": "#66ffe0",
        "green": "#00ff66",
        "green-light": "#66ff99",
        "yellow": "#ffcc00",
        "orange": "#ff00aa",
        "coral": "#f78c6c",
        "teal": "#00ffaa",
        "red": "#ff3366",
        "text": "#f8f8f2",
        "text-muted": "#d0c5e0",
        "text-disabled": "#8c86a8",
        "text-on-accent": "#0f0c1a",
        "muted": "#7a7a9c",
        "muted-dark": "#4a4a68",
        "white": "#ffffff",
        "off-white": "#f5f0ff",
        "bg": "#0f0c1a",
        "bg-card": "#171225",
        "bg-elevated": "#1f1733",
        "bg-sidebar": "#08060f",
        "divider": "#2e2348",
        "glow": "#ff00cc",
    },
    "soft": {
        "primary": "#e892ff",
        "primary-light": "#f1b8ff",
        "primary-dark": "#c06edd",
        "pink": "#ff99dd",
        "pink-light": "#ffc2ff",
        "magenta": "#ff99ff",
        "cyan": "#99ffee",
        "cyan-light": "#c2fff5",
        "green": "#66ff99",
        "green-light": "#99ffbb",
        "yellow": "#ffe699",
        "orange": "#ffb38c",
        "coral": "#ff99dd",
        "teal": "#80ffcc",
        "red": "#ff6677",
        "text": "#f0ecf8",
        "text-muted": "#c8c0db",
        "text-disabled": "#8c86a8",
        "text-on-accent": "#1a1626",
        "muted": "#8c8cb0",
        "muted-dark": "#5a5a7a",
        "white": "#ffffff",
        "off-white": "#f5f0ff",
        "bg": "#1a1626",
        "bg-card": "#241f33",
        "bg-elevated": "#2e2845",
        "bg-sidebar": "#141220",
        "divider": "#3e3456",
        "glow": "#ff99dd",
    },
    "glow": {
        "primary": "#ff00ff",
        "primary-light": "#ff66ff",
        "primary-dark": "#cc66ff",
        "pink": "#ff66ff",
        "pink-light": "#ff99ff",
        "magenta": "#ff00ff",
        "cyan": "#00ffff",
        "cyan-light": "#66ffff",
        "green": "#00ff00",
        "green-light": "#66ff66",
        "yellow": "#ffff00",
        "orange": "#ff66ff",
        "coral": "#ff66ff",
        "teal": "#00ffcc",
        "red": "#ff0066",
        "text": "#ffffff",
        "text-muted": "#cc99ff",
        "text-disabled": "#9977bb",
        "text-on-accent": "#000000",
        "muted": "#666666",
        "muted-dark": "#444444",
        "white": "#ffffff",
        "off-white": "#f0e6ff",
        "bg": "#0a0816",
        "bg-card": "#14091f",
        "bg-elevated": "#1a0033",
        "bg-sidebar": "#000000",
        "divider": "#2a0a44",
        "glow": "#ff00ff",
    },
    "dawn": {
        "primary": "#7e2bd5",
        "primary-light": "#9654e0",
        "primary-dark": "#5e1ba8",
        "pink": "#b40077",
        "pink-light": "#c04a8f",
        "magenta": "#b40077",
        "cyan": "#007f8e",
        "cyan-light": "#009fae",
        "green": "#2d8659",
        "green-light": "#38a169",
        "yellow": "#a88600",
        "orange": "#c05621",
        "coral": "#c74a8c",
        "teal": "#1f9e7a",
        "red": "#c1272d",
        "text": "#2b2540",
        "text-muted": "#5a4d6e",
        "text-disabled": "#8e84a8",
        "text-on-accent": "#ffffff",
        "muted": "#8e84a8",
        "muted-dark": "#6b5f80",
        "white": "#ffffff",
        "off-white": "#faf8ff",
        "bg": "#faf8ff",
        "bg-card": "#ffffff",
        "bg-elevated": "#f1ecff",
        "bg-sidebar": "#f1ecff",
        "divider": "#e0d6f5",
        "glow": "#b40077",
    },
}

# Themes registered in the HA picker. (display name, palette key).
FLAT_THEMES = [
    ("SilkCircuit", "neon"),
    ("SilkCircuit Vibrant", "vibrant"),
    ("SilkCircuit Soft", "soft"),
    ("SilkCircuit Glow", "glow"),
    ("SilkCircuit Dawn", "dawn"),
]
# Auto follows the OS light/dark setting: Dawn by day, Neon by night.
AUTO_NAME = "SilkCircuit Auto"

# All visual rules. Resolves entirely through var(--color-*), so it is identical
# for every variant; only __CARD_MOD_THEME__ is substituted per theme. Authored
# at indent 2 (theme level); card-mod literal blocks indent their content to 4.
BODY = """\
  card-mod-theme: __CARD_MOD_THEME__

  # ============================================
  # CORE COLORS — purple primary, pink emphasis
  # ============================================
  primary-color: var(--color-primary)
  light-primary-color: var(--color-primary-light)
  dark-primary-color: var(--color-primary-dark)
  accent-color: var(--color-pink)
  light-accent-color: var(--color-pink-light)
  secondary-color: var(--color-cyan)

  # Dashboard-facing palette aliases
  purple-color: var(--color-primary)
  pink-color: var(--color-pink)
  light-pink-color: var(--color-pink-light)
  dark-pink-color: var(--color-primary-dark)
  magenta-color: var(--color-magenta)
  blue-color: var(--color-cyan)
  cyan-color: var(--color-cyan)
  green-color: var(--color-green)
  yellow-color: var(--color-yellow)
  red-color: var(--color-red)
  orange-color: var(--color-orange)
  coral-color: var(--color-coral)
  teal-color: var(--color-teal)

  # Status
  info-color: var(--color-cyan)
  success-color: var(--color-green)
  warning-color: var(--color-yellow)
  error-color: var(--color-red)

  # ============================================
  # BACKGROUNDS
  # ============================================
  primary-background-color: var(--color-bg)
  secondary-background-color: var(--color-bg-card)
  card-background-color: var(--color-bg-card)
  ha-card-background: var(--color-bg-card)
  divider-color: var(--color-divider)
  paper-dialog-background-color: var(--color-bg-card)
  markdown-code-background-color: var(--color-bg-elevated)
  code-editor-background-color: var(--color-bg-elevated)
  material-background-color: var(--color-bg-card)
  material-secondary-background-color: var(--color-bg-elevated)
  table-row-background-color: var(--color-bg-card)
  table-row-alternative-background-color: var(--color-bg-elevated)
  data-table-background-color: var(--color-bg)

  # ============================================
  # TEXT — roles invert for the light (Dawn) variant
  # ============================================
  text-primary-color: var(--color-text)
  primary-text-color: var(--color-text)
  text-secondary-color: var(--color-text-muted)
  secondary-text-color: var(--color-text-muted)
  text-accent-color: var(--color-text-on-accent)
  text-dark-color: var(--color-text-on-accent)
  text-very-light-color: var(--color-text)
  disabled-text-color: var(--color-text-disabled)
  app-header-text-color: var(--color-text)
  paper-card-header-color: var(--color-text)
  paper-card-header-text-color: var(--color-text)
  paper-font-headline_-_color: var(--color-text)
  paper-font-subhead_-_color: var(--color-text-muted)
  paper-font-body1_-_color: var(--color-text)
  paper-font-caption_-_color: var(--color-text-muted)
  paper-grey-50: var(--color-text)
  paper-grey-200: var(--color-bg-card)

  # ============================================
  # SIDEBAR & HEADER
  # ============================================
  sidebar-background-color: var(--color-bg-sidebar)
  sidebar-icon-color: var(--color-primary)
  sidebar-text-color: var(--color-text)
  sidebar-selected-background-color: rgba(var(--color-primary-rgb), 0.25)
  sidebar-selected-icon-color: var(--color-pink)
  sidebar-selected-text-color: var(--color-text)
  app-header-background-color: var(--color-bg)
  app-header-edit-background-color: rgba(var(--color-primary-rgb), 0.3)
  paper-drawer-background-color: var(--color-bg-sidebar)
  paper-drawer-text-color: var(--color-text)
  paper-drawer-selected-color: var(--color-primary)
  paper-menu-background-color: var(--color-bg-card)
  paper-menu-color: var(--color-text)
  paper-menu-disabled-color: var(--color-text-disabled)

  # ============================================
  # CARDS & STATE
  # ============================================
  ha-card-border-radius: "12px"
  ha-card-box-shadow: "0 2px 4px 0 rgba(0,0,0,0.16), 0 2px 10px 0 rgba(0,0,0,0.12), 0 0 12px rgba(var(--color-glow-rgb), 0.3)"
  paper-card-background-color: var(--color-bg-card)
  state-icon-color: var(--color-primary)
  state-icon-active-color: var(--color-pink)
  state-icon-unavailable-color: var(--color-muted-dark)
  state-on-color: var(--color-green)
  state-off-color: var(--color-red)
  state-idle-color: var(--color-cyan)
  state-standby-color: var(--color-orange)
  state-unknown-color: var(--color-muted)
  paper-item-icon-color: var(--color-primary)
  paper-item-icon-active-color: var(--color-pink)
  paper-item-icon_-_color: var(--color-primary)
  paper-item-min-height: "36px"
  paper-item-selected_-_background-color: rgba(var(--color-primary-rgb), 0.3)
  paper-item-selected_-_color: var(--color-text)
  paper-item-hover_-_background-color: rgba(var(--color-primary-rgb), 0.1)
  paper-item-focused_-_background-color: rgba(var(--color-primary-rgb), 0.1)
  paper-item-focused-before_-_opacity: "0.12"
  paper-icon-item_-_background-color: "transparent"

  # ============================================
  # CONTROLS — sliders, switches, toggles
  # ============================================
  paper-slider-knob-color: var(--color-primary)
  paper-slider-knob-start-color: var(--color-muted)
  paper-slider-pin-color: var(--color-primary)
  paper-slider-active-color: var(--color-primary)
  paper-slider-secondary-color: var(--color-pink)
  paper-slider-container-color: rgba(var(--color-muted-rgb), 0.4)
  switch-checked-button-color: var(--color-primary)
  switch-checked-track-color: rgba(var(--color-primary-rgb), 0.6)
  switch-unchecked-button-color: var(--color-muted)
  switch-unchecked-track-color: rgba(var(--color-muted-rgb), 0.4)
  paper-toggle-button-checked-button-color: var(--color-primary)
  paper-toggle-button-checked-bar-color: rgba(var(--color-primary-rgb), 0.6)
  paper-toggle-button-unchecked-button-color: var(--color-muted)
  paper-toggle-button-unchecked-bar-color: rgba(var(--color-muted-rgb), 0.4)
  paper-progress-active-color: var(--color-primary)
  paper-progress-container-color: rgba(var(--color-muted-rgb), 0.4)
  paper-progress-disabled-active-color: var(--color-text-disabled)
  paper-progress-secondary-color: var(--color-pink)
  paper-spinner-color: var(--color-primary)
  paper-spinner-layer-1-color: var(--color-primary)
  paper-spinner-layer-2-color: var(--color-green)
  paper-spinner-layer-3-color: var(--color-pink)
  paper-spinner-layer-4-color: var(--color-cyan)

  # ============================================
  # DROPDOWNS, MENUS & TABS
  # ============================================
  paper-listbox-background-color: var(--color-bg-card)
  paper-listbox-color: var(--color-text)
  paper-dropdown-menu-color: var(--color-text)
  paper-dropdown-menu-label-color: var(--color-text-muted)
  input-dropdown-icon-color: var(--color-primary)
  mdc-select-fill-color: var(--color-bg-card)
  mdc-select-ink-color: var(--color-text)
  mdc-select-label-ink-color: var(--color-text-muted)
  mdc-select-idle-line-color: var(--color-primary)
  mdc-select-dropdown-icon-color: var(--color-primary)
  mdc-select-hover-line-color: var(--color-pink)
  mdc-text-field-label-ink-color: var(--color-text)
  paper-tabs-selection-bar-color: var(--color-primary)
  paper-tab-ink: var(--color-primary)
  paper-tabs-container-color: "transparent"
  paper-tabs-content-container_-_background-color: "transparent"
  paper-tabs-selection-bar_-_border-color: var(--color-primary)

  # ============================================
  # FORMS & INPUTS
  # ============================================
  input-fill-color: "rgba(var(--color-text-rgb), 0.06)"
  input-ink-color: var(--color-text)
  input-label-ink-color: var(--color-text-muted)
  input-disabled-ink-color: var(--color-text-disabled)
  input-disabled-fill-color: "rgba(var(--color-text-rgb), 0.02)"
  input-idle-line-color: var(--color-primary)
  input-hover-line-color: var(--color-pink)
  input-disabled-line-color: var(--color-muted-dark)
  input-outlined-idle-border-color: var(--color-primary)
  input-outlined-hover-border-color: var(--color-pink)
  input-outlined-disabled-border-color: var(--color-muted-dark)
  paper-input-container-color: var(--color-text-muted)
  paper-input-container-focus-color: var(--color-primary)
  paper-input-container-invalid-color: var(--color-red)
  paper-input-container-input-color: var(--color-text)
  paper-checkbox-checkmark-color: var(--color-text-on-accent)
  paper-checkbox-checked-color: var(--color-primary)
  paper-checkbox-checked-ink-color: var(--color-primary)
  paper-checkbox-unchecked-color: var(--color-primary)
  paper-checkbox-unchecked-ink-color: var(--color-primary)
  paper-checkbox-label-color: var(--color-text)
  paper-checkbox-label-checked-color: var(--color-text)
  paper-checkbox-disabled-color: var(--color-muted-dark)
  paper-checkbox-disabled-ink-color: var(--color-muted-dark)
  mdc-checkbox-unchecked-color: var(--color-muted)
  paper-radio-button-checked-color: var(--color-primary)
  paper-radio-button-checked-ink-color: var(--color-primary)
  paper-radio-button-unchecked-color: var(--color-primary)
  paper-radio-button-unchecked-ink-color: var(--color-primary)
  paper-radio-button-label-color: var(--color-text)
  paper-radio-button-disabled-color: var(--color-muted-dark)
  paper-button-active-keyboard-focus-background: rgba(var(--color-primary-rgb), 0.3)
  paper-button-disabled-text-color: var(--color-text-disabled)
  paper-button-disabled_-_background-color: rgba(var(--color-muted-rgb), 0.15)
  paper-button-disabled_-_color: var(--color-text-disabled)
  paper-button-raised-keyboard-focus_-_background-color: rgba(var(--color-primary-rgb), 0.2)
  paper-dialog-button-color: var(--color-primary)

  # ============================================
  # MDC THEMING
  # ============================================
  mdc-theme-primary: var(--color-primary)
  mdc-theme-secondary: var(--color-pink)
  mdc-theme-background: var(--color-bg)
  mdc-theme-surface: var(--color-bg-card)
  mdc-theme-on-primary: var(--color-text-on-accent)
  mdc-theme-on-secondary: var(--color-text-on-accent)
  mdc-theme-on-surface: var(--color-text)

  # ============================================
  # CHIPS, DIALOGS, BADGES
  # ============================================
  paper-chip-background-color: var(--color-bg-card)
  paper-chip-icon-color: var(--color-primary)
  paper-chip-text-color: var(--color-text)
  paper-chip-selected-background-color: rgba(var(--color-primary-rgb), 0.3)
  paper-chip-selected-text-color: var(--color-text)
  paper-toast-background-color: var(--color-bg-card)
  paper-datepicker-ink-color: var(--color-text)
  paper-datepicker-accent-color: var(--color-primary)
  paper-datepicker-toggled-color: var(--color-primary)
  paper-datepicker-disabled-color: var(--color-muted-dark)
  paper-datepicker-calendar-color: var(--color-bg-card)
  label-badge-red: var(--color-red)
  label-badge-green: var(--color-green)
  label-badge-blue: var(--color-cyan)
  label-badge-yellow: var(--color-yellow)
  label-badge-gray: var(--color-muted)
  label-badge-text-color: var(--color-text)
  label-badge-background-color: rgba(var(--color-bg-card-rgb), 0.8)

  # ============================================
  # DOMAIN-SPECIFIC
  # ============================================
  energy-grid-consumption-color: var(--color-red)
  energy-grid-return-color: var(--color-green)
  energy-solar-color: var(--color-yellow)
  energy-battery-in-color: var(--color-cyan)
  energy-battery-out-color: var(--color-orange)
  energy-gas-color: var(--color-red)
  energy-water-color: var(--color-cyan)
  history-graph-color: var(--color-pink)
  light-color: var(--color-yellow)
  logbook-entry-color: var(--color-pink)
  media-upload-hover-color: rgba(var(--color-primary-rgb), 0.3)
  mini-media-player-base-color: var(--color-yellow)
  mini-media-player-accent-color: var(--color-pink)
  svg-card-presets-color: var(--color-text)
  weather-day-color: var(--color-yellow)
  weather-night-color: var(--color-cyan)
  climate-heat-color: var(--color-red)
  climate-cool-color: var(--color-cyan)
  climate-fan-only-color: var(--color-green)
  climate-auto-color: var(--color-primary)
  climate-dry-color: var(--color-orange)
  climate-idle-color: var(--color-text-muted)
  climate-off-color: var(--color-muted-dark)
  plant-ok-color: var(--color-green)
  plant-problem-color: var(--color-red)
  scrollbar-thumb-color: var(--color-divider)

  # ============================================
  # CARD-MOD — the electric layer (glow, gradients)
  # ============================================
  card-mod-root: |
    :root {
      --sc-glow: rgba(var(--color-glow-rgb), 0.3);
      --sc-glow-strong: rgba(var(--color-glow-rgb), 0.5);
      --sc-border: rgba(var(--color-primary-rgb), 0.2);
      --sc-border-light: rgba(var(--color-primary-rgb), 0.3);
      --sc-shadow-normal: rgba(0, 0, 0, 0.3);
      --sc-shadow-strong: rgba(0, 0, 0, 0.5);
    }
    ha-sidebar {
      background: linear-gradient(to bottom, var(--color-bg-sidebar), var(--color-bg)) !important;
      border-right: 1px solid var(--sc-border);
      box-shadow: 3px 0 15px var(--sc-shadow-strong);
    }
    [role="heading"], div.header {
      color: var(--color-text) !important;
      text-shadow: 0 0 8px var(--sc-glow) !important;
    }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--color-bg); border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: var(--color-divider); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--sc-glow-strong); }
    ha-card { transition: all 0.3s ease; }
    ha-card:hover {
      box-shadow: 0 5px 15px var(--sc-shadow-normal), 0 0 15px var(--sc-glow-strong) !important;
      transform: translateY(-2px);
    }
  card-mod-card: |
    ha-card { border: 1px solid var(--sc-border-light); }
    .card-header { text-shadow: 0 0 8px var(--sc-glow); }
    .card-content { padding: 16px; }
    .entity-row { position: relative; overflow: hidden; }
    .entity-row:after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 1px;
      background: linear-gradient(to right, transparent, var(--sc-border-light), transparent);
    }
  card-mod-view: |
    .type-custom-button-card,
    .type-entities,
    .type-custom-hui-entities-card,
    .type-history-graph,
    .type-media-control,
    .type-weather-forecast {
      --ha-card-box-shadow: 0 2px 5px 0 var(--sc-shadow-normal);
      --ha-card-border-radius: 12px;
      --ha-card-background: var(--card-background-color);
      margin-bottom: 10px;
    }
    .column > * { margin-bottom: 12px; }
    #view {
      background-image: radial-gradient(circle at 50% 50%, var(--sc-glow), rgba(0, 0, 0, 0) 70%);
    }
  card-mod-more-info: |
    .mdc-dialog .mdc-dialog__container .mdc-dialog__surface {
      border: 1px solid var(--sc-border-light);
      box-shadow: 0 0 20px var(--sc-glow);
      background: linear-gradient(145deg, var(--card-background-color), var(--primary-background-color));
    }
    .mdc-dialog .mdc-dialog__scrim {
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      background: rgba(0, 0, 0, 0.5) !important;
    }
    .mdc-dialog .mdc-dialog__title {
      color: var(--color-text);
      text-shadow: 0 0 8px var(--sc-glow);
    }
    .mdc-dialog .mdc-dialog__actions button { color: var(--color-pink); }
    .mdc-dialog__container { filter: drop-shadow(0 0 10px var(--sc-border)); }
  card-mod-button: |
    ha-icon-button, ha-button {
      color: var(--color-pink);
      transition: all 0.2s ease;
    }
    ha-icon-button:hover, ha-button:hover {
      color: var(--color-pink-light);
      filter: brightness(1.2) drop-shadow(0 0 5px var(--sc-glow-strong));
    }
  card-mod-form: |
    ha-textfield, ha-selector, ha-select {
      --mdc-theme-primary: var(--color-primary);
    }
    ha-textfield:focus-within, ha-selector:focus-within, ha-select:focus-within {
      --mdc-theme-primary: var(--color-pink);
    }
    ha-form-actions mwc-button {
      --mdc-theme-primary: var(--color-primary);
    }
"""


def hex_to_rgb(value: str) -> str:
    """'#e135ff' -> '225, 53, 255'."""
    h = value.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected 6-digit hex, got {value!r}")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"{r}, {g}, {b}"


def color_block(palette_key: str, indent: int) -> str:
    """Emit `--color-<token>` and `--color-<token>-rgb` lines for a variant."""
    pal = PALETTES[palette_key]
    missing = [k for k in TOKEN_ORDER if k not in pal]
    if missing:
        raise ValueError(f"palette {palette_key!r} missing tokens: {missing}")
    sp = " " * indent
    lines = [f"{sp}# SilkCircuit {palette_key} palette"]
    for key in TOKEN_ORDER:
        hexv = pal[key]
        lines.append(f'{sp}--color-{key}: "{hexv}"')
        lines.append(f'{sp}--color-{key}-rgb: "{hex_to_rgb(hexv)}"')
    return "\n".join(lines) + "\n"


def body_for(theme_name: str) -> str:
    return BODY.replace("__CARD_MOD_THEME__", theme_name)


def reindent(block: str, spaces: int) -> str:
    """Shift a 2-space-indented block to a deeper indent (for modes nesting)."""
    pad = " " * (spaces - 2)
    return "".join(
        (pad + line if line.strip() else line)
        for line in block.splitlines(keepends=True)
    )


def check_tokens() -> None:
    """Every var(--color-*) the body references must exist in every palette."""
    referenced = set(re.findall(r"var\(--color-([a-zA-Z0-9_-]+?)(?:-rgb)?\)", BODY))
    known = set(TOKEN_ORDER)
    unknown = referenced - known
    if unknown:
        raise SystemExit(f"BODY references undefined color tokens: {sorted(unknown)}")


def build() -> str:
    check_tokens()
    out = [
        "# SilkCircuit — a neon dream for Home Assistant",
        "#",
        "# GENERATED FILE — do not edit by hand.",
        "# Source of truth: scripts/build_theme.py (palettes from silkcircuit-nvim).",
        "# Regenerate:  python3 scripts/build_theme.py",
        "#",
        "# Variants: SilkCircuit (neon), Vibrant, Soft, Glow, Dawn (light), Auto.",
        "",
    ]
    for name, key in FLAT_THEMES:
        out.append(f"{name}:")
        out.append(color_block(key, indent=2).rstrip("\n"))
        out.append(body_for(name).rstrip("\n"))
        out.append("")

    # Auto: shared body at theme level, palette swapped per light/dark mode.
    out.append(f"{AUTO_NAME}:")
    out.append(body_for(AUTO_NAME).rstrip("\n"))
    out.append("  modes:")
    out.append("    dark:")
    out.append(reindent(color_block("neon", indent=2), 6).rstrip("\n"))
    out.append("    light:")
    out.append(reindent(color_block("dawn", indent=2), 6).rstrip("\n"))
    out.append("")
    return "\n".join(out) + "\n"


def main() -> int:
    content = build()
    OUT.write_text(content, encoding="utf-8")
    theme_count = len(FLAT_THEMES) + 1
    print(
        f"✨ wrote {OUT.relative_to(OUT.parent.parent)} — {theme_count} themes, {len(content.splitlines())} lines"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
