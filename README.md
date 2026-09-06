# Qtile Configuration

Personal [Qtile](https://qtile.org/) setup for X11 (Wayland‑aware).
Tokyo Night colour palette, a bottom status bar with custom widgets, sticky
windows, and a full minimize / restore workflow.

- **Config file:** `config.py`
- **Mod key:** `Super` (a.k.a. `mod4` / Windows key)
- **Terminal:** `alacritty`
- **Bar font:** `FiraCode Nerd Font Mono`

---

## Table of contents

1. [Dependencies](#dependencies)
2. [Keybindings](#keybindings)
3. [Mouse bindings](#mouse-bindings)
4. [Layouts](#layouts)
5. [Groups / workspaces](#groups--workspaces)
6. [Status bar & widgets](#status-bar--widgets)
7. [Custom widgets](#custom-widgets)
8. [Sticky windows](#sticky-windows)
9. [Minimize / restore workflow](#minimize--restore-workflow)
10. [Hooks & autostart](#hooks--autostart)
11. [General behaviour settings](#general-behaviour-settings)
12. [Reloading & troubleshooting](#reloading--troubleshooting)
13. [Known cosmetic issues](#known-cosmetic-issues)

---

## Dependencies

### Required

| Command | Used for |
|---|---|
| `alacritty` | Default terminal |
| `picom` | Compositor (started on login, config at `~/.config/picom/picom.conf`) |
| `FiraCode Nerd Font Mono` | Bar text and glyph icons |
| `xset`, `xsetroot` | Solid background, keyboard LEDs, screen‑blank / DPMS timers |
| `pactl` | Mute toggle (PulseAudio / PipeWire) |
| `playerctl` | Media key controls |
| `flameshot` | Screenshots |

### Optional (features degrade gracefully if missing)

| Command | Used for |
|---|---|
| `rofi` | Preferred menu for the "restore minimized window" picker |
| `dmenu` | Fallback menu when `rofi` is not installed |
| `htop` | Opened when the CPU widget is clicked |
| `pavucontrol` | Opened when the Volume widget is clicked |
| `nm-connection-editor` | Opened when the Network widget is clicked |
| `firefox`, `discord`, `spotify` | Bar launcher icons |
| PS2 emulator at `/home/facu/Documentos/Emulador/ps2` | `Super + p` |

---

## Keybindings

`Super` = mod key.

### Window management

| Shortcut | Action |
|---|---|
| `Super + w` | Close focused window |
| `Super + f` | Toggle fullscreen |
| `Super + Shift + f` | Toggle floating |
| `Super + m` | Maximize within the current layout |
| `Super + n` | Reset all window sizes in the layout (normalize) |
| `Super + s` | Toggle **sticky** state on the focused window |
| `Super + d` | Minimize / un‑minimize the focused window |
| `Super + Shift + d` | Open a menu to pick which minimized window to restore |
| `Super + Ctrl + d` | Restore **all** minimized windows in the current group |

### Focus

| Shortcut | Action |
|---|---|
| `Super + ←/→/↓/↑` | Move focus in that direction |
| `Super + Tab` | Focus next window in the layout |

### Move / resize windows

| Shortcut | Action |
|---|---|
| `Super + Shift + ←/→/↓/↑` | Shuffle (move) the window in that direction |
| `Super + Ctrl + ←/→/↓/↑` | Grow the window towards that edge |
| `Super + Shift + Return` | Toggle split / stacked in the Columns layout |

### Layouts

| Shortcut | Action |
|---|---|
| `Super + Shift + Tab` | Cycle to the next layout |

### Groups (workspaces)

| Shortcut | Action |
|---|---|
| `Super + [1‑9]` | Switch to group N |
| `Super + Shift + [1‑9]` | Move focused window to group N and follow it |
| `Super + q` | Previous group |
| `Super + e` | Next group |

### Applications & launchers

| Shortcut | Action |
|---|---|
| `Super + Return` | Open terminal (`alacritty`) |
| `Super + r` | Command prompt in the bar (`spawncmd`) |
| `Super + p` | Launch the PS2 emulator |

### Media & audio

| Shortcut | Action |
|---|---|
| `Super + space` | Play / pause (`playerctl`) |
| `Super + .` | Next track |
| `Super + ,` | Previous track |
| `Super + Shift + m` | Toggle mute on the default sink |

### Screenshots

| Shortcut | Action |
|---|---|
| `Print` | `flameshot gui` (region selection) |
| `Super + Print` | `flameshot screen` (whole screen) |

### Keyboard LEDs

| Shortcut | Action |
|---|---|
| `Super + Scroll_Lock` | Turn keyboard LEDs on (`xset led on`) |
| `Super + Shift + Scroll_Lock` | Turn keyboard LEDs off |

### Qtile session

| Shortcut | Action |
|---|---|
| `Super + Ctrl + r` | Reload the config |
| `Super + Ctrl + q` | Quit Qtile |

### Virtual terminals (Wayland only)

| Shortcut | Action |
|---|---|
| `Ctrl + Alt + F1 … F7` | Switch to VT 1‑7 (ignored on X11) |

---

## Mouse bindings

| Gesture | Action |
|---|---|
| `Super + Left‑drag` | Move a floating window |
| `Super + Right‑drag` | Resize a floating window |
| `Super + Middle‑click` | Bring the window to the front |

`follow_mouse_focus` is enabled, so the window under the pointer is focused
automatically.

---

## Layouts

| Layout | Notes |
|---|---|
| `Columns` | Default. 2 px borders, accent‑blue focus border, 3 px gaps. Supports split/stacked columns (`Super + Shift + Return`). |
| `Max` | Single full‑area window. |

### Floating rules

The following always float (in addition to Qtile's built‑in defaults):

`firefox-esr`, `Picture-in-Picture`, `confirmreset`, `makebranch`, `maketag`,
`ssh-askpass`, `branchdialog`, `pinentry`.

Floating windows are kept above tiled ones (`floats_kept_above = True`).

---

## Groups / workspaces

Nine groups, named `1`–`9`. See the [Groups keybindings](#groups-workspaces)
above. The `GroupBox` widget at the far left of the bar shows them; scrolling
the mouse wheel over it also switches group.

---

## Status bar & widgets

A single **bottom bar**, 32 px tall, semi‑transparent dark background
(`opacity = 0.5`) with a 1 px border.

Left → right:

| Widget | Description | Click action |
|---|---|---|
| `GroupBox` | Workspaces 1‑9, block highlight | Left‑click a group to switch; mouse wheel to cycle |
| Firefox icon | Launcher | Launch `firefox` |
| Discord icon | Launcher | Launch `discord` |
| Terminal icon | Launcher | Launch `alacritty` |
| Spotify icon | Launcher | Launch `spotify` |
| `Prompt` | Input line for `Super + r` | — |
| **`MinimizedWindows`** | Custom. Shows `󰖰 N · title, title …` for minimized windows in the current group; hidden when there are none | **Left‑click:** open the restore menu (or restore directly if only one). **Right‑click:** restore all |
| `Spacer` | Pushes the rest to the right | — |
| **`CPU`** | `󰻠 NN%` total CPU load, refreshed every 1 s | Left‑click: open `htop` in a terminal |
| `Memory` | `MemUsed / MemTotal` in GB, refreshed every 1 s | — |
| `ThermalSensor` | CPU temperature; turns red above 60 °C | — |
| `Volume` | Current output volume | Left‑click: open `pavucontrol` |
| **`NetworkWidget`** | Custom. Auto‑detected interface + live down/up speed | Left‑click: open `nm-connection-editor` |
| `Clock` | `HH:MM` | — |
| `Clock` | `DD/MM/YYYY` | — |

---

## Custom widgets

### `NetworkWidget`

Subclass of `widget.GenPollText`, polled every 2 s.

- Scans `/sys/class/net/` and picks the first non‑loopback interface whose
  `operstate` is `up`.
- Reads `rx_bytes` / `tx_bytes` and reports the delta as a speed:
  `KB/s` under 1 MB/s, `MB/s` otherwise (`󰖩 ↓… ↑…`).
- Shows `󰤭 Sin red` when no interface is up and re‑detects automatically if the
  link changes.

### `MinimizedWindows`

Subclass of `widget.GenPollText`, polled every 1 s.

- Lists only the **minimized** windows of the current group.
- Returns an empty string (so the widget is invisible) when nothing is
  minimized.
- **Left‑click** → `_pick_minimized()`; **Right‑click** → restore all.

---

## Sticky windows

A "sticky" window is visible on **every** group and follows you as you switch.

- `Super + s` toggles sticky on the focused window.
- Firefox **Picture‑in‑Picture** windows are made sticky automatically
  (`client_managed` hook).
- Sticky windows are re‑parented to the active group on every group change
  without stealing focus (`setgroup` hook), and removed from the tracking list
  when closed (`client_killed` hook).

Implementation: a module‑level `sticky_windows` list plus the
`toggle_sticky_windows` lazy function.

---

## Minimize / restore workflow

Because a minimized window disappears from the layout, several ways to bring it
back are provided:

| Trigger | Behaviour |
|---|---|
| `Super + d` | `toggle_minimize` on the focused window |
| `Super + Ctrl + d` | `unminimize_all` – clears `minimized` on every window in the group |
| `Super + Shift + d` | `pick_minimized` – interactive picker |
| `MinimizedWindows` widget | Left‑click = picker, right‑click = restore all |

### `pick_minimized` internals

1. Collects minimized windows of the current group.
2. If none → does nothing; if exactly one → restores it directly.
3. Otherwise builds an `index: title` list and feeds it to **`rofi -dmenu`**
   (preferred) or **`dmenu`** (fallback).
4. The menu runs in a **background thread** so Qtile's event loop never blocks.
5. The chosen window is restored back on the Qtile thread via
   `call_soon_threadsafe` (`_restore_window`: un‑minimize → switch to its group
   → focus it).

`auto_minimize = True` is also set, so applications that request minimize via
`_NET_WM_STATE_HIDDEN` (window‑manager buttons, taskbar protocols) are honoured.

---

## Hooks & autostart

| Hook | What it does |
|---|---|
| `startup_once` | Starts `picom`; paints a solid `#1a1b26` root window with `xsetroot`; sets screen‑blank and DPMS timers to 5400 s (90 min) via `xset` |
| `setgroup` | Moves sticky windows into the newly‑active group |
| `client_killed` | Removes closed windows from the sticky list |
| `client_managed` | Auto‑stickies Firefox Picture‑in‑Picture windows |

---

## General behaviour settings

| Setting | Value | Effect |
|---|---|---|
| `follow_mouse_focus` | `True` | Focus follows the pointer |
| `bring_front_click` | `False` | Clicking a window does not raise it automatically |
| `floats_kept_above` | `True` | Floating windows stay above tiled ones |
| `cursor_warp` | `False` | Pointer is not moved when focus changes |
| `auto_fullscreen` | `True` | Honour client fullscreen requests |
| `focus_on_window_activation` | `"smart"` | Focus new windows only when appropriate |
| `reconfigure_screens` | `True` | Re‑run screen config on monitor hot‑plug |
| `auto_minimize` | `True` | Honour client minimize requests |
| `wmname` | `"LG3D"` | Java AWT compatibility workaround |
| `wl_xcursor_theme` / `wl_xcursor_size` | `None` / `24` | Wayland cursor defaults |

---

## Reloading & troubleshooting

```bash
# Validate the config without applying it
qtile check

# Reload in a running session
Super + Ctrl + r
```

If Qtile fails to start, check `~/.local/share/qtile/qtile.log`.

---

## Known cosmetic issues

- The glyph characters inside several **icon `TextBox` widgets** in the bar
  (Firefox / Discord / terminal / Spotify launchers, and the Memory, Thermal
  and Volume icons) are currently empty in `config.py` – the icons do not
  render. The CPU icon (`󰻠`) and the clock / calendar icons use Material Design
  code points and do render correctly. Restoring the missing glyphs is a
  cosmetic fix only; functionality (click actions, readings) is unaffected.
