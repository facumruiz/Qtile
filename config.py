# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# MIT License

import os
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# ===== CONFIGURACIÓN INICIAL =====
mod = "mod4"
terminal = guess_terminal()


# ===== STICKY WINDOWS (VENTANAS PEGAJOSAS) =====
sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    """Alternar estado sticky de una ventana"""
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window


# ===== HOOKS =====
@hook.subscribe.startup_once
def autostart():
    os.system("picom --config ~/.config/picom/picom.conf &")


@hook.subscribe.setgroup
def move_sticky_windows():
    """Mover ventanas sticky al grupo actual SIN robar el foco"""
    for window in sticky_windows:
        window.togroup(switch_group=False)  # ← Clave: switch_group=False


@hook.subscribe.client_killed
def remove_sticky_windows(window):
    """Limpiar ventanas sticky cuando se cierran"""
    if window in sticky_windows:
        sticky_windows.remove(window)


@hook.subscribe.client_managed
def auto_sticky_windows(window):
    """Hacer Picture-in-Picture automáticamente sticky"""
    info = window.info()
    # Para Firefox en español el nombre puede variar
    if (info['wm_class'] and 'firefox' in str(info['wm_class']).lower()
            and info['name'] and 'picture-in-picture' in info['name'].lower()):
        sticky_windows.append(window)


# ===== PALETA DE COLORES =====
colors = {
    "background": "#1a1b26",
    "foreground": "#a9b1d6",
    "accent": "#7aa2f7",
    "secondary": "#9ece6a",
    "secondary-memory": "#9ece6a2d",
    "alert": "#f7768e3b",
    "cyan": "#7dcfff",
    "purple": "#bb9af7",
    "yellow": "#e0af68",
    "gray": "#565f89",
    "dark_gray": "#24283b",
    "dark-purple": "#9e7cd839",
    "deep-purple": "#5133865C",
    "spotify": "#5f9b7471",
    "border": "#414868",
}

# ===== DISEÑOS =====
layouts = [
    layout.Columns(
        border_focus=colors["accent"],
        border_normal=colors["dark_gray"],
        border_width=2,
        margin=3,
    ),
    layout.Max(),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="firefox-esr"),
        Match(title="Picture-in-Picture"),
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
    border_focus=colors["accent"],
    border_normal=colors["dark_gray"],
    border_width=2,
)

# ===== ATAJOS DE TECLADO =====
keys = [
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "s", toggle_sticky_windows(), desc="Toggle sticky window"),  # ← NUEVO
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
    Key([mod], "space", lazy.layout.next(), desc="Cambiar foco a otra ventana"),
    Key(
        [mod, "shift"],
        "Left",
        lazy.layout.shuffle_left(),
        desc="Mover ventana a la izquierda",
    ),
    Key(
        [mod, "shift"],
        "Right",
        lazy.layout.shuffle_right(),
        desc="Mover ventana a la derecha",
    ),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Mover ventana abajo"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Mover ventana arriba"),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        desc="Expandir ventana a la izquierda",
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        desc="Expandir ventana a la derecha",
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        desc="Expandir ventana hacia abajo",
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        desc="Expandir ventana hacia arriba",
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalizar tamaño de ventanas"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Alternar entre vistas divididas",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Cambiar de diseño"),
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),
    Key([mod], "m", lazy.layout.maximize(), desc="Maximizar en el layout"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Pantalla completa"),
    Key([mod], "r", lazy.spawncmd(), desc="Ejecutar comando"),
    Key(
        [mod, "control"],
        "r",
        lazy.reload_config(),
        desc="Recargar configuración de Qtile",
    ),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Apagar Qtile"),
    Key([mod], "q", lazy.screen.prev_group(), desc="Cambiar al grupo anterior"),
    Key([mod], "e", lazy.screen.next_group(), desc="Cambiar al siguiente grupo"),
    Key(
        [mod],
        "p",
        lazy.spawn("/home/facu/Documentos/Emulador/ps2"),
        desc="Abrir emulador de PS2",
    ),
    Key(
        [mod],
        "Scroll_Lock",
        lazy.spawn("xset led on"),
        desc="Encender luces del teclado",
    ),
    Key(
        [mod, "shift"],
        "Scroll_Lock",
        lazy.spawn("xset led off"),
        desc="Apagar luces del teclado",
    ),
    Key(
        [mod, "shift"],
        "m",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Silenciar/activar sonido",
    ),
    Key([mod], "n", lazy.spawn("playerctl next"), desc="Siguiente pista"),
    Key(
        [mod],
        "b",
        lazy.spawn("playerctl previous"),
        desc="Retroceder a la pista anterior",
    ),
    Key([mod], "space", lazy.spawn("playerctl play-pause"), desc="Reproducir/Pausar"),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "Print", lazy.spawn("flameshot screen")),
]

# Add VT switching for Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# ===== GRUPOS =====
groups = [Group(i) for i in "123456789"]

# Emoji inicial
emoji_inactivo = "󰈈"
emoji_activo = "󰈉"

# Etiquetar grupos inicialmente
for i in groups:
    i.label = emoji_inactivo
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )


# Hook simple para cambiar el emoji del grupo activo
@hook.subscribe.setgroup
def cambiar_emoji(grupo):
    for g in qtile.groups:
        g.label = emoji_activo if g == grupo else emoji_inactivo


# ===== CONFIGURACIÓN DE WIDGETS =====
widget_defaults = dict(
    font="FiraCode Nerd Font Mono",
    fontsize=30,
    padding=3,
)
extension_defaults = widget_defaults.copy()

groupbox_settings = {
    "font": "FiraCode Nerd Font Mono",
    "fontsize": 30,
    "margin_y": 3,
    "margin_x": 0,
    "padding_y": 5,
    "padding_x": 3,
    "borderwidth": 3,
    "active": colors["foreground"],
    "inactive": colors["gray"],
    "rounded": False,
    "highlight_color": colors["dark_gray"],
    "highlight_method": "block",
    "this_current_screen_border": colors["deep-purple"],
    "this_screen_border": colors["dark-purple"],
    "other_current_screen_border": colors["dark_gray"],
    "other_screen_border": colors["dark_gray"],
    "foreground": colors["foreground"],
    "background": colors["dark_gray"],
    "disable_drag": True,
    "toggle": True,
    "use_mouse_wheel": True,
}

# ===== PANTALLAS Y BARRAS =====
screens = [
    Screen(
        wallpaper="~/Imágenes/fondos/tool.webp",
        wallpaper_mode="stretch",
        bottom=bar.Bar(
            [
                widget.GroupBox(**groupbox_settings),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=30,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("firefox")},
                ),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=30,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("discord")},
                ),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=30,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(terminal)},
                ),
                widget.TextBox(text="­", padding=3),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=30,
                    foreground=colors["foreground"],
                    padding=3,
                    border_width=10,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("spotify")},
                ),
                # widget.Mpris2(
                #     name="spotify",
                #     objname="org.mpris.MediaPlayer2.spotify",
                #     display_metadata=["xesam:title", "xesam:artist"],
                #     scroll=True,
                #     scroll_interval=0.05,
                #     scroll_delay=2,
                #     width=150,
                #     foreground=colors["foreground"],
                #     playing_text="{track}",
                #     paused_text="{track}",
                #     fontsize=13,
                #     padding=5,
                #     mouse_callbacks={
                #         "Button1": lambda: qtile.cmd_spawn("playerctl play-pause"),
                #         "Button3": lambda: qtile.cmd_spawn("spotify"),
                #         "Button4": lambda: qtile.cmd_spawn("playerctl next"),
                #         "Button5": lambda: qtile.cmd_spawn("playerctl previous"),
                #     },
                # ),
                widget.TextBox(text="­", padding=3),
                widget.Prompt(fontsize=15, foreground=colors["purple"]),
                widget.Spacer(length=bar.STRETCH),
                widget.Memory(
                    format="{MemUsed: .1f}G |{MemTotal: .1f}G",
                    font="FiraCode Nerd Font Mono",
                    foreground=colors["cyan"],
                    background=colors["dark_gray"],
                    fontsize=13,
                    padding=8,
                    measure_mem="G",
                    update_interval=1.0,
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark_gray"]),
                widget.TextBox(
                    text="­", padding=4, background=colors["secondary-memory"]
                ),
                widget.ThermalSensor(
                    foreground=colors["secondary"],
                    foreground_alert=colors["alert"],
                    background=colors["secondary-memory"],
                    threshold=60,
                    fmt="{}",
                    fontsize=13,
                    padding=8,
                ),
                widget.TextBox(
                    text="­", padding=3, background=colors["secondary-memory"]
                ),
                widget.TextBox(text="­", padding=3),
                widget.TextBox(
                    text="",
                    fontsize=20,
                ),
                widget.Volume(
                    fmt="{}",
                    font="FiraCode Nerd Font Mono",
                    foreground=colors["foreground"],
                    fontsize=14,
                    padding=8,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("pavucontrol")},
                ),
                widget.TextBox(text="­", padding=3),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
                widget.TextBox(
                    text="󰥔",
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    fontsize=20,
                ),
                widget.Clock(
                    format="%H:%M",
                    font="FiraCode Nerd Font Mono",
                    fontsize=14,
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    markup=True,
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
                widget.TextBox(
                    text="󰃭",
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    fontsize=20,
                ),
                widget.Clock(
                    format="%d/%m/%Y",
                    font="FiraCode Nerd Font Mono",
                    fontsize=14,
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    markup=True,
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
            ],
            28,
            background=colors["dark_gray"] + "80",
            margin=[0, 300, 0, 300],
            border_color=colors["border"],
            border_width=[1, 1, 1, 1],
            opacity=0.5,
        ),
    ),
]

# ===== CONFIGURACIÓN DEL RATÓN =====
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ===== CONFIGURACIÓN GENERAL =====
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# ===== CONFIGURACIÓN WAYLAND =====
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"
