# MIT License

import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# ===== CONFIGURACIÓN INICIAL =====
mod = "mod4"
terminal = "alacritty"

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

# ===== STICKY WINDOWS (VENTANAS PEGAJOSAS) =====
sticky_windows = []


@lazy.function
def unminimize_all(qtile):
    """Restaurar todas las ventanas minimizadas del grupo actual"""
    for window in qtile.current_group.windows:
        if window.minimized:
            window.minimized = False


def _restore_window(qtile, win):
    """Restaurar y enfocar una ventana concreta (llamar desde el hilo de qtile)"""
    try:
        if win.minimized:
            win.minimized = False
        win.group.toscreen()
        win.group.focus(win, True)
    except Exception:
        pass


def _pick_minimized(qtile):
    """Elegir con un menú (rofi/dmenu) qué ventana minimizada restaurar"""
    import shutil
    import subprocess
    import threading

    wins = [w for w in qtile.current_screen.group.windows if w.minimized]
    if not wins:
        return
    if len(wins) == 1:
        _restore_window(qtile, wins[0])
        return

    entries = [f"{i}: {(w.name or 'sin nombre')[:60]}" for i, w in enumerate(wins)]
    menu = "\n".join(entries)

    if shutil.which("rofi"):
        cmd = ["rofi", "-dmenu", "-i", "-p", "Restaurar"]
    else:
        cmd = ["dmenu", "-i", "-l", "10", "-p", "Restaurar:"]

    def run():
        try:
            res = subprocess.run(
                cmd, input=menu, capture_output=True, text=True
            )
        except Exception:
            return
        choice = res.stdout.strip()
        if not choice or ":" not in choice:
            return
        try:
            idx = int(choice.split(":", 1)[0])
        except ValueError:
            return
        if 0 <= idx < len(wins):
            win = wins[idx]
            try:
                qtile.call_soon_threadsafe(_restore_window, qtile, win)
            except AttributeError:
                _restore_window(qtile, win)

    threading.Thread(target=run, daemon=True).start()


pick_minimized = lazy.function(_pick_minimized)


@lazy.function
def toggle_sticky_windows(qtile, window=None):
    """Alternar estado sticky de una ventana"""
    if window is None:
        window = qtile.current_screen.group.current_window
    if window is None:
        return

    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)


# ===== HOOKS =====
@hook.subscribe.startup_once
def autostart():
    """Iniciar compositor al arranque y setear fondo de color sólido"""
    os.system("picom --config ~/.config/picom/picom.conf &")
    os.system("sleep 0.3 && xsetroot -solid '#1a1b26' &")
    os.system("xset s 5400 5400")
    os.system("xset dpms 5400 5400 5400")


@hook.subscribe.setgroup
def move_sticky_windows():
    """Mover ventanas sticky al grupo actual sin robar foco"""
    for window in sticky_windows[:]:  # Copia de la lista para evitar problemas
        if window and window.group:
            window.togroup(switch_group=False)


@hook.subscribe.client_killed
def remove_sticky_windows(window):
    """Limpiar ventanas sticky cuando se cierran"""
    if window in sticky_windows:
        sticky_windows.remove(window)


@hook.subscribe.client_managed
def auto_sticky_windows(window):
    """Hacer Picture-in-Picture automáticamente sticky"""
    try:
        info = window.info()
        wm_class = str(info.get("wm_class", "")).lower()
        name = str(info.get("name", "")).lower()

        if "firefox" in wm_class and "picture-in-picture" in name:
            if window not in sticky_windows:
                sticky_windows.append(window)
    except Exception:
        pass  # Evitar crashes si la ventana se cierra antes de procesarse


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
    # Sticky windows
    Key([mod], "s", toggle_sticky_windows, desc="Toggle sticky window"),
    # Gestión de ventanas
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "w", lazy.window.kill(), desc="Cerrar ventana"),
    Key([mod], "m", lazy.layout.maximize(), desc="Maximizar en el layout"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Pantalla completa"),
    Key([mod], "d", lazy.window.toggle_minimize(), desc="Minimizar/restaurar ventana"),
    Key(
        [mod, "shift"],
        "d",
        pick_minimized,
        desc="Elegir qué ventana minimizada restaurar (menú)",
    ),
    Key(
        [mod, "control"],
        "d",
        unminimize_all,
        desc="Restaurar todas las ventanas minimizadas",
    ),
    # Navegación con flechas
    Key([mod], "Left", lazy.layout.left(), desc="Mover foco a la izquierda"),
    Key([mod], "Right", lazy.layout.right(), desc="Mover foco a la derecha"),
    Key([mod], "Down", lazy.layout.down(), desc="Mover foco abajo"),
    Key([mod], "Up", lazy.layout.up(), desc="Mover foco arriba"),
    Key([mod], "Tab", lazy.layout.next(), desc="Cambiar foco a otra ventana"),
    # Mover ventanas
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
    # Redimensionar ventanas
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
    # Layouts
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Alternar entre vistas divididas",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Abrir terminal"),
    Key([mod, "shift"], "Tab", lazy.next_layout(), desc="Cambiar de diseño"),
    # Qtile
    Key([mod], "r", lazy.spawncmd(), desc="Ejecutar comando"),
    Key(
        [mod, "control"],
        "r",
        lazy.reload_config(),
        desc="Recargar configuración de Qtile",
    ),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Apagar Qtile"),
    # Grupos
    Key([mod], "q", lazy.screen.prev_group(), desc="Cambiar al grupo anterior"),
    Key([mod], "e", lazy.screen.next_group(), desc="Cambiar al siguiente grupo"),
    # Aplicaciones
    Key(
        [mod],
        "p",
        lazy.spawn("/home/facu/Documentos/Emulador/ps2"),
        desc="Abrir emulador de PS2",
    ),
    # Teclado
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
    # Audio
    Key(
        [mod, "shift"],
        "m",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Silenciar/activar sonido",
    ),
    # Control multimedia
    Key([mod], "period", lazy.spawn("playerctl next"), desc="Siguiente pista"),
    Key([mod], "comma", lazy.spawn("playerctl previous"), desc="Pista anterior"),
    Key([mod], "space", lazy.spawn("playerctl play-pause"), desc="Reproducir/Pausar"),
    # Screenshots
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot con selección"),
    Key(
        [mod],
        "Print",
        lazy.spawn("flameshot screen"),
        desc="Screenshot pantalla completa",
    ),
]

# VT switching para Wayland
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

for group in groups:
    keys.extend(
        [
            Key(
                [mod],
                group.name,
                lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}",
            ),
            Key(
                [mod, "shift"],
                group.name,
                lazy.window.togroup(group.name, switch_group=True),
                desc=f"Switch to & move focused window to group {group.name}",
            ),
        ]
    )

# ===== CONFIGURACIÓN DE WIDGETS =====
widget_defaults = {
    "font": "FiraCode Nerd Font Mono",
    "fontsize": 16,
    "padding": 5,
}
extension_defaults = widget_defaults.copy()

groupbox_settings = {
    "font": "FiraCode Nerd Font Mono",
    "fontsize": 20,
    "margin_y": 3,
    "margin_x": 0,
    "padding_y": 8,
    "padding_x": 5,
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


# ===== FUNCIÓN AUXILIAR PARA CALLBACKS =====
def make_callback(command):
    """Factory para crear callbacks de mouse"""
    return lambda: qtile.cmd_spawn(command)


# ===== WIDGET PERSONALIZADO DE RED =====
class NetworkWidget(widget.GenPollText):
    """Widget personalizado que muestra estado de red y velocidad"""

    def __init__(self, **config):
        widget.GenPollText.__init__(self, **config)
        self.update_interval = 2
        self.interface = None
        self.rx_old = None
        self.tx_old = None

    def get_active_interface(self):
        """Detectar la interfaz de red activa"""
        import os

        try:
            net_path = "/sys/class/net/"
            if os.path.exists(net_path):
                for iface in os.listdir(net_path):
                    if iface == "lo":
                        continue
                    operstate_file = os.path.join(net_path, iface, "operstate")
                    if os.path.exists(operstate_file):
                        with open(operstate_file, "r") as f:
                            state = f.read().strip()
                            if state == "up":
                                return iface
            return None
        except:
            return None

    def poll(self):
        import os

        try:
            if self.interface is None:
                self.interface = self.get_active_interface()

            if self.interface is None:
                return "󰤭 Sin red"

            rx_file = f"/sys/class/net/{self.interface}/statistics/rx_bytes"
            tx_file = f"/sys/class/net/{self.interface}/statistics/tx_bytes"

            if not (os.path.exists(rx_file) and os.path.exists(tx_file)):
                self.interface = None
                return "󰤭 Sin red"

            with open(rx_file, "r") as f:
                rx_new = int(f.read().strip())
            with open(tx_file, "r") as f:
                tx_new = int(f.read().strip())

            if self.rx_old is not None and self.tx_old is not None:
                rx_speed = (rx_new - self.rx_old) / (1024 * 1024 * self.update_interval)
                tx_speed = (tx_new - self.tx_old) / (1024 * 1024 * self.update_interval)

                self.rx_old = rx_new
                self.tx_old = tx_new

                if rx_speed >= 1 or tx_speed >= 1:
                    return f"󰖩 ↓{rx_speed:.1f} ↑{tx_speed:.1f}MB/s"
                else:
                    rx_kb = rx_speed * 1024
                    tx_kb = tx_speed * 1024
                    return f"󰖩 ↓{rx_kb:.0f} ↑{tx_kb:.0f}KB/s"
            else:
                self.rx_old = rx_new
                self.tx_old = tx_new
                return f"󰖩 {self.interface}"

        except Exception as e:
            self.interface = None
            self.rx_old = None
            self.tx_old = None
            return "󰤭 Error"


# ===== WIDGET PERSONALIZADO DE VENTANAS MINIMIZADAS =====
class MinimizedWindows(widget.GenPollText):
    """Muestra únicamente las ventanas minimizadas del grupo actual.

    Click izquierdo: abre un menú (rofi/dmenu) para elegir cuál restaurar.
                     Si solo hay una, la restaura directamente.
    Click derecho: restaura todas.
    Si no hay ninguna minimizada, el widget queda vacío (invisible).
    """

    def __init__(self, **config):
        widget.GenPollText.__init__(self, **config)
        self.update_interval = 1
        self.add_callbacks(
            {
                "Button1": self.pick,
                "Button3": self.restore_all,
            }
        )

    def _minimized(self):
        try:
            return [w for w in qtile.current_screen.group.windows if w.minimized]
        except Exception:
            return []

    def poll(self):
        wins = self._minimized()
        if not wins:
            return ""
        names = ", ".join((w.name or "sin nombre")[:20] for w in wins)
        return f"󰖰 {len(wins)} · {names}"

    def pick(self):
        _pick_minimized(qtile)

    def restore_all(self):
        for w in self._minimized():
            w.minimized = False


# ===== PANTALLAS Y BARRAS =====
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(**groupbox_settings),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=22,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": make_callback("firefox")},
                ),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=22,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": make_callback("discord")},
                ),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=22,
                    foreground=colors["foreground"],
                    padding=8,
                    mouse_callbacks={"Button1": make_callback(terminal)},
                ),
                widget.TextBox(text="­", padding=3),
                widget.TextBox(
                    text="",
                    font="FiraCode Nerd Font Mono",
                    fontsize=22,
                    foreground=colors["foreground"],
                    padding=3,
                    mouse_callbacks={"Button1": make_callback("spotify")},
                ),
                widget.TextBox(text="­", padding=3),
                widget.Prompt(fontsize=16, foreground=colors["purple"]),
                MinimizedWindows(
                    font="FiraCode Nerd Font Mono",
                    fontsize=14,
                    foreground=colors["yellow"],
                    padding=8,
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.TextBox(
                    text="󰻠",
                    font="FiraCode Nerd Font Mono",
                    fontsize=18,
                    foreground=colors["accent"],
                    background=colors["dark_gray"],
                    padding=5,
                ),
                widget.CPU(
                    format="{load_percent:.0f}%",
                    font="FiraCode Nerd Font Mono",
                    foreground=colors["accent"],
                    background=colors["dark_gray"],
                    fontsize=15,
                    padding=8,
                    update_interval=1.0,
                    mouse_callbacks={
                        "Button1": make_callback(f"{terminal} -e htop")
                    },
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark_gray"]),
                widget.TextBox(
                    text="",
                    fontsize=18,
                    foreground=colors["cyan"],
                    background=colors["dark_gray"],
                    padding=5,
                ),
                widget.Memory(
                    format="{MemUsed: .1f}G |{MemTotal: .1f}G",
                    font="FiraCode Nerd Font Mono",
                    foreground=colors["cyan"],
                    background=colors["dark_gray"],
                    fontsize=15,
                    padding=8,
                    measure_mem="G",
                    update_interval=1.0,
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark_gray"]),
                widget.TextBox(
                    text="­", padding=4, background=colors["secondary-memory"]
                ),
                widget.TextBox(
                    text="",
                    fontsize=18,
                    foreground=colors["secondary"],
                    background=colors["secondary-memory"],
                    padding=5,
                ),
                widget.ThermalSensor(
                    foreground=colors["secondary"],
                    foreground_alert=colors["alert"],
                    background=colors["secondary-memory"],
                    threshold=60,
                    fmt="{}",
                    fontsize=15,
                    padding=8,
                ),
                widget.TextBox(
                    text="­", padding=3, background=colors["secondary-memory"]
                ),
                widget.TextBox(text="­", padding=3),
                widget.TextBox(text="", fontsize=18),
                widget.Volume(
                    fmt="{}",
                    font="FiraCode Nerd Font Mono",
                    foreground=colors["foreground"],
                    fontsize=16,
                    padding=8,
                    mouse_callbacks={"Button1": make_callback("pavucontrol")},
                ),
                widget.TextBox(text="­", padding=3),
                NetworkWidget(
                    foreground=colors["cyan"],
                    background=colors["dark_gray"],
                    fontsize=15,
                    padding=8,
                    mouse_callbacks={"Button1": make_callback("nm-connection-editor")},
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
                widget.TextBox(
                    text="󰥔",
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    fontsize=18,
                ),
                widget.Clock(
                    format="%H:%M",
                    font="FiraCode Nerd Font Mono",
                    fontsize=16,
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
                widget.TextBox(
                    text="󰃭",
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                    fontsize=18,
                ),
                widget.Clock(
                    format="%d/%m/%Y",
                    font="FiraCode Nerd Font Mono",
                    fontsize=16,
                    background=colors["dark-purple"],
                    foreground=colors["purple"],
                ),
                widget.TextBox(text="­", padding=3, background=colors["dark-purple"]),
            ],
            32,
            background=colors["dark_gray"] + "80",
            margin=[0, 0, 0, 0],
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
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"
