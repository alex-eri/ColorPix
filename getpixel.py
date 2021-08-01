import gi
from pprint import pprint
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

display = Gdk.Display.get_default()
color_chooser = Gtk.ColorChooserWidget()
color_chooser.props.show_editor = True
xentry = Gtk.Entry()
yentry = Gtk.Entry()
xbox = Gtk.Box(spacing=10)
xbox.pack_start(Gtk.Label(label="x"), False, True, 0)
xbox.pack_start(xentry, True, True, 0)
ybox = Gtk.Box(spacing=10)
ybox.pack_start(Gtk.Label(label="y"), False, True, 0)
ybox.pack_start(yentry, True, True, 0)

def on_press(widget, event, *a):
    window = widget.props.window
    if display.get_window_at_pointer()[0] == window:
        return 
    geom = window.get_geometry()
    x, y = int(geom.x + event.x), int(geom.y + event.y)
    root = widget.get_screen().get_root_window()
    color = Gdk.pixbuf_get_from_window(root, x, y, 1, 1).get_pixels()
    c = f"#{color.hex()}"
    print((x, y, c))
    gcolor =  Gdk.RGBA()
    gcolor.parse(c)
    color_chooser.set_rgba(gcolor)
    xentry.set_text(f'{x}')
    yentry.set_text(f'{y}')
   
def grab(widget, *a):
    dwin = widget.get_window()
    pointer = display.get_default_seat().get_pointer()
    status = pointer.grab(dwin, Gdk.GrabOwnership.NONE, True, Gdk.EventMask.BUTTON_PRESS_MASK, Gdk.Cursor.new_from_name(display, 'cell'), Gdk.CURRENT_TIME)

def ungrab(widget, *a):
    display.get_default_seat().ungrab()

mainwin = Gtk.Window()
hb = Gtk.HeaderBar()
hb.set_show_close_button(True)
hb.props.title = "Color picker"
mainwin.set_titlebar(hb)
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
box.pack_start(xbox, False, True, 0)
box.pack_start(ybox, False, True, 0)
box.pack_start(color_chooser, True, True, 0)
box.props.margin = 10
mainwin.add(box)
mainwin.connect("destroy", Gtk.main_quit)
mainwin.connect("focus-in-event", grab)
mainwin.connect("enter-notify-event", ungrab)
mainwin.connect("leave-notify-event", grab)
mainwin.show_all()
mainwin.set_keep_above(True)
mainwin.connect("button_press_event", on_press)

Gtk.main()
