# Qtile Configuration

This is a custom configuration for Qtile, a dynamic window manager written in Python. This setup defines various keybindings, layouts, widgets, and functionality to create a personalized and productive desktop environment.

## Features

- **Custom Keybindings:** Key combinations for managing windows, switching between layouts, launching applications, and controlling media playback.
- **Multiple Layouts:** Includes column-based and maximized window layouts.
- **Widget Bar:** A bottom bar with useful widgets such as group boxes, a window name display, clock, and media controls for Spotify.
- **Floating Window Management:** Includes drag, resize, and bring-to-front functionality for floating windows.

## Keybindings

### Window Management

- **Focus Movement:**  
  - `Mod + Left/Right/Down/Up` - Move focus between windows.
  - `Mod + Space` - Switch focus to the next window.
  
- **Window Positioning:**  
  - `Mod + Shift + Arrow Keys` - Move window around the layout.
  
- **Resize Windows:**  
  - `Mod + Ctrl + Arrow Keys` - Resize windows in the layout.

- **Floating Mode:**  
  - `Mod + Shift + F` - Toggle floating mode for the focused window.

### Layout Management

- `Mod + Shift + Return` - Toggle split layout.
- `Mod + Tab` - Switch to the next layout.

### Application Shortcuts

- `Mod + Return` - Open terminal.
- `Mod + P` - Open PS2 Emulator.

### Media Controls

- `Mod + M` - Mute/Unmute audio.
- `Mod + Space` - Play/Pause media.
- `Mod + N/B` - Next/Previous track.

### System Controls

- `Mod + Ctrl + R` - Reload Qtile configuration.
- `Mod + Ctrl + Q` - Quit Qtile.

## Groups

This configuration uses five workspace groups (`1`, `2`, `3`, `4`, `5`):

- Switch to a group: `Mod + GroupNumber`
- Move window to a group and switch: `Mod + Shift + GroupNumber`

## Layouts

Qtile supports multiple layouts. The following layouts are defined:

- **Columns Layout:** With adjustable borders and the ability to manage windows in columns.
- **Max Layout:** Maximizes windows without overlapping.

## Widgets

The bottom bar includes the following widgets:

- **GroupBox:** Displays the current workspace group.
- **Prompt:** For executing commands.
- **WindowName:** Shows the name of the focused window.
- **Spotify Widget:** Displays the current song playing on Spotify.
- **Clock:** Shows date and time in the format `DD/MM/YYYY | HH:MM`.
- **QuickExit:** A button to log out or quit Qtile.

## Floating Windows

Specific applications and dialogs are set to always float:

- GitK dialogs (`makebranch`, `maketag`)
- SSH password prompt (`ssh-askpass`)
- GPG key password entry (`pinentry`)

## Custom Colors

The configuration includes a custom color palette used for widgets and background elements:

- **Spotify Green:** `#1db954`
- **Red:** `#ab3333`
- **Dark Green:** `#14532d`
- **Lime Green:** `#82e776`
- **White:** `#ffffff`
- **Light Gray:** `#f0f0f0`
- **Black:** `#191414`
- **Hour Color:** `#45112b`

