#!/usr/bin/env python3
"""Control de ventanas X11 (XWayland) para manejar WinUnisoft bajo Wine.

Solo biblioteca estándar + ctypes (libX11, libXtst) y PIL para guardar PNG.

Uso:
  wusctl.py ventanas                     lista ventanas con título (id, x, y, ancho, alto, título)
  wusctl.py captura [salida.png] [--ventana TEXTO]    captura la ventana (por defecto, WinUnisoft)
  wusctl.py clic X Y [--doble] [--derecho] [--ventana TEXTO]  X, Y relativos a la ventana cliente
  wusctl.py escribir "texto" [--ventana TEXTO]         escribe texto (ASCII)
  wusctl.py tecla Return|Escape|Tab|F5|ctrl+o|alt+f ... [--ventana TEXTO]

Los clics y teclas van con XSendEvent directo a la ventana de Wine (XWayland ignora XTest
en GNOME sin sesión de escritorio remoto). La captura es de la ventana, no de la pantalla.
  wusctl.py simular "TP 7-1" "Alfil TP.prj"   abre el proyecto, lo simula y muestra el .ERR
  wusctl.py activar TEXTO                trae al frente la ventana cuyo título contiene TEXTO
"""
import ctypes
import ctypes.util
import os
import sys
import time

DISPLAY = os.environ.get("DISPLAY", ":0")

x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11") or "libX11.so.6")
xtst = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Xtst") or "libXtst.so.6")

Window = ctypes.c_ulong
Atom = ctypes.c_ulong


class XImage(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int), ("height", ctypes.c_int), ("xoffset", ctypes.c_int),
                ("format", ctypes.c_int), ("data", ctypes.POINTER(ctypes.c_char)),
                ("byte_order", ctypes.c_int), ("bitmap_unit", ctypes.c_int),
                ("bitmap_bit_order", ctypes.c_int), ("bitmap_pad", ctypes.c_int),
                ("depth", ctypes.c_int), ("bytes_per_line", ctypes.c_int),
                ("bits_per_pixel", ctypes.c_int), ("red_mask", ctypes.c_ulong),
                ("green_mask", ctypes.c_ulong), ("blue_mask", ctypes.c_ulong)]


class XWindowAttributes(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int), ("width", ctypes.c_int),
                ("height", ctypes.c_int), ("border_width", ctypes.c_int), ("depth", ctypes.c_int),
                ("visual", ctypes.c_void_p), ("root", Window), ("class", ctypes.c_int),
                ("bit_gravity", ctypes.c_int), ("win_gravity", ctypes.c_int),
                ("backing_store", ctypes.c_int), ("backing_planes", ctypes.c_ulong),
                ("backing_pixel", ctypes.c_ulong), ("save_under", ctypes.c_int),
                ("colormaps", ctypes.c_ulong), ("map_installed", ctypes.c_int),
                ("map_state", ctypes.c_int), ("all_event_masks", ctypes.c_long),
                ("your_event_mask", ctypes.c_long), ("do_not_propagate_mask", ctypes.c_long),
                ("override_redirect", ctypes.c_int), ("screen", ctypes.c_void_p)]


x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XDefaultRootWindow.restype = Window
x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
x11.XGetImage.restype = ctypes.POINTER(XImage)
x11.XGetImage.argtypes = [ctypes.c_void_p, Window, ctypes.c_int, ctypes.c_int, ctypes.c_uint,
                          ctypes.c_uint, ctypes.c_ulong, ctypes.c_int]
x11.XQueryTree.argtypes = [ctypes.c_void_p, Window, ctypes.POINTER(Window), ctypes.POINTER(Window),
                           ctypes.POINTER(ctypes.POINTER(Window)), ctypes.POINTER(ctypes.c_uint)]
x11.XGetWindowAttributes.argtypes = [ctypes.c_void_p, Window, ctypes.POINTER(XWindowAttributes)]
x11.XTranslateCoordinates.argtypes = [ctypes.c_void_p, Window, Window, ctypes.c_int, ctypes.c_int,
                                      ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                                      ctypes.POINTER(Window)]
x11.XFetchName.argtypes = [ctypes.c_void_p, Window, ctypes.POINTER(ctypes.c_char_p)]
x11.XInternAtom.restype = Atom
x11.XInternAtom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
x11.XGetWindowProperty.argtypes = [ctypes.c_void_p, Window, Atom, ctypes.c_long, ctypes.c_long,
                                   ctypes.c_int, Atom, ctypes.POINTER(Atom),
                                   ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_ulong),
                                   ctypes.POINTER(ctypes.c_ulong),
                                   ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
x11.XKeysymToKeycode.restype = ctypes.c_ubyte
x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
x11.XStringToKeysym.restype = ctypes.c_ulong
x11.XStringToKeysym.argtypes = [ctypes.c_char_p]
x11.XRaiseWindow.argtypes = [ctypes.c_void_p, Window]
x11.XSetInputFocus.argtypes = [ctypes.c_void_p, Window, ctypes.c_int, ctypes.c_ulong]
x11.XFlush.argtypes = [ctypes.c_void_p]
x11.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]
x11.XDestroyImage = None  # se libera con XFree sobre data (no hace falta en un proceso corto)
xtst.XTestFakeMotionEvent.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulong]
xtst.XTestFakeButtonEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]
xtst.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]

d = x11.XOpenDisplay(DISPLAY.encode())
if not d:
    sys.exit("No se pudo abrir el display X %s" % DISPLAY)
ROOT = x11.XDefaultRootWindow(d)

# ignorar errores X (p. ej. BadWindow cuando un diálogo se cierra entre la pulsación y la
# liberación de una tecla); sin esto Xlib termina el proceso
_MANEJADOR = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(lambda dd, ev: 0)
x11.XSetErrorHandler.argtypes = [ctypes.c_void_p]
x11.XSetErrorHandler(_MANEJADOR)


def titulo(w):
    """_NET_WM_NAME (UTF-8) o WM_NAME."""
    a = x11.XInternAtom(d, b"_NET_WM_NAME", 0)
    utf8 = x11.XInternAtom(d, b"UTF8_STRING", 0)
    t, f, n, r = Atom(), ctypes.c_int(), ctypes.c_ulong(), ctypes.c_ulong()
    p = ctypes.POINTER(ctypes.c_ubyte)()
    if x11.XGetWindowProperty(d, w, a, 0, 1024, 0, utf8, ctypes.byref(t), ctypes.byref(f),
                              ctypes.byref(n), ctypes.byref(r), ctypes.byref(p)) == 0 and n.value:
        return bytes(p[:n.value]).decode("utf-8", "replace")
    s = ctypes.c_char_p()
    if x11.XFetchName(d, w, ctypes.byref(s)) and s.value:
        return s.value.decode("latin-1")
    return ""


def hijos(w):
    r, p = Window(), Window()
    ch = ctypes.POINTER(Window)()
    n = ctypes.c_uint()
    if not x11.XQueryTree(d, w, ctypes.byref(r), ctypes.byref(p), ctypes.byref(ch), ctypes.byref(n)):
        return []
    return [ch[i] for i in range(n.value)]


def geometria(w):
    at = XWindowAttributes()
    x11.XGetWindowAttributes(d, w, ctypes.byref(at))
    x, y, c = ctypes.c_int(), ctypes.c_int(), Window()
    x11.XTranslateCoordinates(d, w, ROOT, 0, 0, ctypes.byref(x), ctypes.byref(y), ctypes.byref(c))
    return x.value, y.value, at.width, at.height, at.map_state == 2


def ventanas():
    out = []
    pila = [ROOT]
    while pila:
        w = pila.pop()
        for c in hijos(w):
            t = titulo(c)
            x, y, an, al, vis = geometria(c)
            if t and vis and an > 20 and al > 20:
                out.append((c, x, y, an, al, t))
            pila.append(c)
    return out


def buscar(texto):
    texto = texto.lower()
    cand = [v for v in ventanas() if texto in v[5].lower()]
    if not cand:
        sys.exit("No hay ventana visible con '%s' en el título" % texto)
    return max(cand, key=lambda v: v[3] * v[4])


def captura(salida, w=None):
    from PIL import Image
    if w is None:
        x, y, an, al, _ = geometria(ROOT)
        win = ROOT
    else:
        win, x, y, an, al = w[0], 0, 0, w[3], w[4]
    img = x11.XGetImage(d, win, 0, 0, an, al, 0xFFFFFFFF, 2)  # ZPixmap
    if not img:
        sys.exit("XGetImage falló")
    im = img.contents
    datos = ctypes.string_at(im.data, im.bytes_per_line * im.height)
    pil = Image.frombuffer("RGBX", (im.width, im.height), datos, "raw", "BGRX", im.bytes_per_line, 1)
    pil.convert("RGB").save(salida)
    print("%s %dx%d" % (salida, im.width, im.height))


def mover(x, y):
    xtst.XTestFakeMotionEvent(d, -1, x, y, 0)
    x11.XSync(d, 0)


def clic(x, y, boton=1, doble=False):
    mover(x, y)
    time.sleep(0.05)
    for _ in range(2 if doble else 1):
        xtst.XTestFakeButtonEvent(d, boton, 1, 0)
        xtst.XTestFakeButtonEvent(d, boton, 0, 0)
        x11.XSync(d, 0)
        time.sleep(0.08)


ALIAS = {"ctrl": "Control_L", "alt": "Alt_L", "shift": "Shift_L", "enter": "Return", "esc": "Escape",
         "supr": "Delete", "del": "Delete", "tab": "Tab", "espacio": "space", "space": "space"}


def keycode(nombre):
    ks = x11.XStringToKeysym(ALIAS.get(nombre.lower(), nombre).encode())
    if not ks:
        sys.exit("Tecla desconocida: %s" % nombre)
    return x11.XKeysymToKeycode(d, ks), ks


def combo(texto):
    """Ej.: 'ctrl+o', 'alt+f', 'Return', 'F5'."""
    teclas = [keycode(t)[0] for t in texto.split("+")]
    for k in teclas:
        xtst.XTestFakeKeyEvent(d, k, 1, 0)
    for k in reversed(teclas):
        xtst.XTestFakeKeyEvent(d, k, 0, 0)
    x11.XSync(d, 0)
    time.sleep(0.05)


SIMBOLOS = {" ": "space", ".": "period", ",": "comma", "-": "minus", "/": "slash", "\\": "backslash",
            ":": "colon", "_": "underscore", "(": "parenleft", ")": "parenright", "%": "percent",
            "\n": "Return", "=": "equal", "+": "plus", ";": "semicolon"}
NECESITA_SHIFT = set(':_()%+') | set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def escribir(texto):
    shift = keycode("Shift_L")[0]
    for ch in texto:
        nombre = SIMBOLOS.get(ch, ch)
        k = keycode(nombre)[0]
        con_shift = ch in NECESITA_SHIFT
        if con_shift:
            xtst.XTestFakeKeyEvent(d, shift, 1, 0)
        xtst.XTestFakeKeyEvent(d, k, 1, 0)
        xtst.XTestFakeKeyEvent(d, k, 0, 0)
        if con_shift:
            xtst.XTestFakeKeyEvent(d, shift, 0, 0)
        x11.XSync(d, 0)
        time.sleep(0.02)


def activar(w):
    x11.XRaiseWindow(d, w[0])
    x11.XSetInputFocus(d, w[0], 2, 0)
    x11.XFlush(d)
    time.sleep(0.2)


# --- eventos sintéticos (XSendEvent) -------------------------------------------------
# En GNOME Wayland, XWayland ignora XTest si no hay una sesión de escritorio remoto
# autorizada; Wine sí acepta eventos enviados con XSendEvent directo a su ventana.
class XButtonEvent(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int), ("serial", ctypes.c_ulong), ("send_event", ctypes.c_int),
                ("display", ctypes.c_void_p), ("window", Window), ("root", Window), ("subwindow", Window),
                ("time", ctypes.c_ulong), ("x", ctypes.c_int), ("y", ctypes.c_int), ("x_root", ctypes.c_int),
                ("y_root", ctypes.c_int), ("state", ctypes.c_uint), ("button", ctypes.c_uint),
                ("same_screen", ctypes.c_int)]


class XKeyEvent(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int), ("serial", ctypes.c_ulong), ("send_event", ctypes.c_int),
                ("display", ctypes.c_void_p), ("window", Window), ("root", Window), ("subwindow", Window),
                ("time", ctypes.c_ulong), ("x", ctypes.c_int), ("y", ctypes.c_int), ("x_root", ctypes.c_int),
                ("y_root", ctypes.c_int), ("state", ctypes.c_uint), ("keycode", ctypes.c_uint),
                ("same_screen", ctypes.c_int)]


class XEvent(ctypes.Union):
    _fields_ = [("xbutton", XButtonEvent), ("xkey", XKeyEvent), ("pad", ctypes.c_long * 24)]


x11.XSendEvent.argtypes = [ctypes.c_void_p, Window, ctypes.c_int, ctypes.c_long, ctypes.POINTER(XEvent)]
SHIFT, CONTROL, MOD1 = 1, 4, 8


def cliente(texto):
    """Ventana cliente (la de Wine, sin el marco de GNOME) con ese título: la más chica de las que coinciden."""
    texto = texto.lower()
    cand = [v for v in ventanas() if texto in v[5].lower()]
    if not cand:
        sys.exit("No hay ventana visible con '%s' en el título" % texto)
    return min(cand, key=lambda v: v[3] * v[4])


def enviar_clic(v, x, y, boton=1, doble=False):
    win, gx, gy = v[0], v[1] + x, v[2] + y
    for _ in range(2 if doble else 1):
        for typ, mask, st in ((4, 1 << 2, 0), (5, 1 << 3, 1 << (7 + boton))):
            e = XEvent()
            b = e.xbutton
            b.type, b.send_event, b.display, b.window, b.root = typ, 1, d, win, ROOT
            b.x, b.y, b.x_root, b.y_root, b.state, b.button, b.same_screen = x, y, gx, gy, st, boton, 1
            x11.XSendEvent(d, win, 1, mask, ctypes.byref(e))
            x11.XSync(d, 0)
            time.sleep(0.06)


def enviar_tecla(v, kc, estado=0):
    for typ, mask in ((2, 1 << 0), (3, 1 << 1)):
        e = XEvent()
        k = e.xkey
        k.type, k.send_event, k.display, k.window, k.root = typ, 1, d, v[0], ROOT
        k.x = k.y = 1
        k.state, k.keycode, k.same_screen = estado, kc, 1
        x11.XSendEvent(d, v[0], 1, mask, ctypes.byref(e))
        x11.XSync(d, 0)
        time.sleep(0.03)


def enviar_combo(v, texto):
    partes = texto.split("+")
    estado = 0
    for m in partes[:-1]:
        estado |= {"ctrl": CONTROL, "control": CONTROL, "alt": MOD1, "shift": SHIFT}[m.lower()]
    enviar_tecla(v, keycode(partes[-1])[0], estado)


def enviar_texto(v, texto):
    for ch in texto:
        kc = keycode(SIMBOLOS.get(ch, ch))[0]
        enviar_tecla(v, kc, SHIFT if ch in NECESITA_SHIFT else 0)


# --- flujo completo: abrir un proyecto y simularlo ---------------------------------
WUS = os.path.expanduser("~/.wine-winunisoft/drive_c/Program Files (x86)/WinUnisoft multicnc")
BOTON = {"abrir": (26, 40), "marcha": (174, 44), "abortar": (268, 44)}


def esperar_ventana(texto, seg=10.0):
    t0 = time.time()
    while time.time() - t0 < seg:
        if any(texto.lower() in v[5].lower() for v in ventanas()):
            return True
        time.sleep(0.3)
    return False


def tecla_segura(v, combo_txt):
    try:
        enviar_combo(v, combo_txt)
    except Exception:
        pass


def simular(subcarpeta, archivo, espera_max=300.0):
    """Abre Proyectos/<subcarpeta>/<archivo> y lo simula; devuelve el texto del .ERR ('' si no hubo)."""
    base = os.path.splitext(archivo)[0].lower()
    carpeta = os.path.join(WUS, "Proyectos", subcarpeta)
    for ext in (".ERR", ".LOG"):
        for f in os.listdir(carpeta):
            if f.lower() == base + ext.lower():
                os.remove(os.path.join(carpeta, f))
    main_v = cliente("WinUnisoft - Simulador")
    enviar_clic(main_v, *BOTON["abortar"])
    time.sleep(1.0)
    for v in ventanas():                      # cerrar un aviso que haya quedado
        if v[5] == "Aviso":
            tecla_segura(v, "Return")
    enviar_clic(cliente("WinUnisoft - Simulador"), *BOTON["abrir"])
    if not esperar_ventana("Abrir..."):
        sys.exit("No se abrió el diálogo Abrir")
    dlg = cliente("Abrir...")
    enviar_texto(dlg, subcarpeta.lower())
    enviar_combo(dlg, "Return")
    time.sleep(1.0)
    enviar_texto(dlg, archivo.lower())
    tecla_segura(dlg, "Return")
    time.sleep(4.0)
    for v in ventanas():
        if v[5] == "Aviso":
            sys.exit("WinUnisoft mostró un aviso al abrir el proyecto")
    enviar_clic(cliente("WinUnisoft - Simulador"), *BOTON["marcha"])
    log = None
    t0 = time.time()
    while time.time() - t0 < espera_max:      # la simulación termina cuando el .LOG deja de crecer
        time.sleep(3.0)
        for f in os.listdir(carpeta):
            if f.lower() == base + ".log":
                log = os.path.join(carpeta, f)
        if log and "Ttime" in open(log, encoding="latin-1").read() and time.time() - os.path.getmtime(log) > 6:
            break
    err = ""
    for f in os.listdir(carpeta):
        if f.lower() == base + ".err":
            err = open(os.path.join(carpeta, f), encoding="latin-1").read().replace("\r", "")
    return err


def opcion(args, nombre):
    if nombre in args:
        i = args.index(nombre)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return None


def main(argv):
    if not argv:
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    vent = opcion(args, "--ventana") or "WinUnisoft"
    if cmd == "ventanas":
        for v in ventanas():
            print("0x%x\t%d,%d\t%dx%d\t%s" % v)
    elif cmd == "captura":
        captura(args[0] if args else "captura.png", cliente(vent))
    elif cmd == "clic":
        nums = [a for a in args if not a.startswith("--")]
        enviar_clic(cliente(vent), int(nums[0]), int(nums[1]), 3 if "--derecho" in args else 1, "--doble" in args)
    elif cmd == "escribir":
        enviar_texto(cliente(vent), args[0])
    elif cmd == "tecla":
        v = cliente(vent)
        for t in args:
            enviar_combo(v, t)
    elif cmd == "simular":
        err = simular(args[0], args[1])
        print(err.strip() or "Sin colisiones ni errores")
    elif cmd == "activar":
        activar(buscar(args[0]))
    else:
        sys.exit("Comando desconocido: " + cmd)


if __name__ == "__main__":
    main(sys.argv[1:])
