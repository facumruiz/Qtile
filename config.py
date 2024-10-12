# Copyright (c) 2010-2014 por múltiples autores
# Bajo la licencia MIT
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


# Configuraciones básicas
mod = "mod4"  # Tecla Mod (Generalmente la tecla Super)
terminal = guess_terminal()

# Teclas de acceso rápido
keys = [
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
    Key([mod], "space", lazy.layout.next(), desc="Cambiar foco a otra ventana"),
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Cambiar de diseño"),
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),
    Key([mod], "r", lazy.spawncmd(), desc="Ejecutar comando"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Recargar configuración de Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Apagar Qtile"),
    Key([mod], "q", lazy.screen.prev_group(), desc="Cambiar al grupo anterior"),
    Key([mod], "e", lazy.screen.next_group(), desc="Cambiar al siguiente grupo"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Alternar pantalla completa"),
    Key([mod], "p", lazy.spawn("/home/facu/Documentos/Emulador/ps2"), desc="Abrir emulador de PS2"),
]


# Grupos de trabajo
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Cambiar al grupo {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Mover ventana al grupo {i.name}"),
    ])

# Diseño de ventanas
layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
]

# Configuración de widgets y barra
widget_defaults = dict(font="sans", fontsize=12, padding=3)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Memory(
                    format='RAM: {MemUsed:.0f}GB / {MemTotal:.0f}GB ({MemPercent:.0f}%)',
                    measure_mem='G',
                    update_interval=1,
                    foreground='ff0000'
                ),
                widget.CPU(
                    format='CPU: {load_percent}%', 
                    update_interval=1, 
                    foreground='00ff00'
                ),
                widget.Prompt(),
                widget.Spacer(),
                widget.Clock(format="%I:%M %a %d-%m-%Y %p"),
                widget.Spacer(),
                mpris2_widget,
                widget.Volume(
                    emoji=True,
                    fmt='Vol: {}',
                    foreground='ffffff',
                ),
                widget.Net(
                    interface='enp3s0',  # Cambia según la interfaz que encontraste
                    format='Subida: {up} ↓↓ Bajada: {down} ↑↑',
                    foreground='ffffff',
                    update_interval=1,  # Intervalo de actualización
                ),

                widget.GroupBox(),
            ],
            25,  # Altura de la barra
        ),
    ),
]

# Configuración para ventanas flotantes y mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),  # gitk
    Match(wm_class="makebranch"),  # gitk
    Match(wm_class="maketag"),  # gitk
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    Match(title="branchdialog"),  # gitk
    Match(title="pinentry"),  # GPG key password entry
])

# Configuraciones adicionales
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"  # Para mejorar compatibilidad con apps Java
