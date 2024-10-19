# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

@hook.subscribe.startup_once
def autostart():
    os.system("picom --config ~/.config/picom/picom.conf &")
    
mod = "mod4"
terminal = guess_terminal()

keys = [
    # Control de ventanas
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
    Key([mod], "space", lazy.layout.next(), desc="Cambiar foco a otra ventana"),

    # Mover y cambiar tamaño de ventanas
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Mover ventana a la izquierda"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Mover ventana a la derecha"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Mover ventana abajo"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Mover ventana arriba"),
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Expandir ventana a la izquierda"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Expandir ventana a la derecha"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Expandir ventana hacia abajo"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Expandir ventana hacia arriba"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalizar tamaño de ventanas"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Alternar entre vistas divididas"),

    # Apertura de aplicaciones
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Cambiar de diseño"),
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),
    
    # Comandos y recarga de configuración
    Key([mod], "r", lazy.spawncmd(), desc="Ejecutar comando"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Recargar configuración de Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Apagar Qtile"),

    # Cambiar de grupo
    Key([mod], "q", lazy.screen.prev_group(), desc="Cambiar al grupo anterior"),
    Key([mod], "e", lazy.screen.next_group(), desc="Cambiar al siguiente grupo"),

    # Maximizar ventana
    Key([mod], "f", lazy.window.toggle_maximize(), desc="Maximizar ventana (sin ocultar barra)"),

    # Acceso a aplicaciones específicas
    Key([mod], "p", lazy.spawn("/home/facu/Documentos/Emulador/ps2"), desc="Abrir emulador de PS2"),
    
    # Control de luces del teclado
    Key([mod], "Scroll_Lock", lazy.spawn("xset led on"), desc="Encender luces del teclado"),
    Key([mod, "shift"], "Scroll_Lock", lazy.spawn("xset led off"), desc="Apagar luces del teclado"),

    # Control de sonido o reproduccion
    Key([mod], "m", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Silenciar/activar sonido"),  # Silenciar
    Key([mod], "n", lazy.spawn("playerctl next"), desc="Siguiente pista"),  # Pasar a la siguiente pista
    Key([mod], "b", lazy.spawn("playerctl previous"), desc="Retroceder a la pista anterior"),  # Retroceder a la pista anterior
    Key([mod], "space", lazy.spawn("playerctl play-pause"), desc="Reproducir/Pausar"),  # Reproducir/Pausar

]



# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

background_paleta = {
    "spotify": "#1db954",  # Verde Spotify
    "rojo": "#ab3333",  # Rojo complementario
    "verde_oscuro": "#14532d",  # Análogo verde oscuro
    "verde_lima": "#82e776",  # Análogo verde claro
    "blanco": "#ffffff",  # Neutro
    "gris_claro": "#f0f0f0",  # Neutro
    "negro": "#191414",  # Neutro oscuro
    "hora": "#45112b",
}

screens = [
    Screen(
        wallpaper='~/Descargas/fondo.jpeg',
        wallpaper_mode='stretch',
        bottom=bar.Bar(
            [
                widget.GroupBox(background=background_paleta["negro"]),
                widget.Prompt(
                    background=background_paleta["blanco"],
                    foreground=background_paleta["negro"],
                ),
                widget.WindowName(background=background_paleta["negro"]),
                widget.Image(
                    filename="~/.config/qtile/icons/spotify.svg",
                    background=background_paleta["negro"],
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("spotify")},
                    scale=True,
                    margin=4.5,  # Espacio alrededor de la imagen
                ),
                widget.Mpris2(
                    name="spotify",
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=["xesam:title", "xesam:artist"],
                    playing_text="{track}  ",
                    paused_text=" Pause ",
                    update_interval=1,
                    max_chars=30,
                    foreground=background_paleta["spotify"],
                    background=background_paleta["negro"],
                ),
                widget.Spacer(
                    foreground=background_paleta["blanco"],
                    background=background_paleta["negro"],
                    length=10,
                ),
                widget.Clock(
                    format="%d/%m/%Y %a %I:%M %p",
                    foreground=background_paleta["blanco"],
                    background=background_paleta["negro"],
                ),
                widget.Spacer(
                    foreground=background_paleta["blanco"],
                    background=background_paleta["rojo"],
                    length=10,
                ),
                widget.QuickExit(
                    default_text="⏻",
                    fontsize=18,
                    background=background_paleta["rojo"],
                    foreground=background_paleta["blanco"],
                ),
                widget.Spacer(
                    foreground=background_paleta["blanco"],
                    background=background_paleta["rojo"],
                    length=10,
                ),
            ],
            24,
        ),
    ),
]
# Drag floating layouts.
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

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
