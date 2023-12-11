#!/bin/python
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib, Gio
import sys
import atexit

#gsettings_pref = Gio.Settings.new("org.gnome.pomodoro.preferences")
#pomodoro_duration = gsettings_pref.get_value("pomodoro-duration")
#short_break_duration = gsettings_pref.get_value("short-break-duration")
#long_break_duration = gsettings_pref.get_value("long-break-duration")

gsettings_state = Gio.Settings.new("org.gnome.pomodoro.state")
state = str(gsettings_state.get_value("timer-state"))
state_duration = int(gsettings_state.get_value("timer-state-duration").get_double())
elapsed = int(gsettings_state.get_value("timer-elapsed").get_double())
is_paused = bool(gsettings_state.get_value("timer-paused"))

state_dict = {"State": state,
              "StateDuration": state_duration,
              "Elapsed": elapsed,
              "IsPaused": is_paused}

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

def bus_handler(_sender=None, contents=None, _=None):
    global state_dict
    #print(contents)

    if "Elapsed" in contents:
        state_dict["Elapsed"] = int(contents["Elapsed"])
        elapsed = state_dict["Elapsed"]
        state_duration = state_dict["StateDuration"]
        print("{: >2}:{:0>2}".format((state_duration - elapsed)// 60, (state_duration - elapsed) % 60), end="\r")
    if "State" in contents:
        state_dict["State"] = str(contents["State"])
    if "StateDuration" in contents:
        state_dict["StateDuration"] = int(contents["StateDuration"])
    if "IsPaused" in contents:
        state_dict["IsPaused"] = bool(contents["IsPaused"])

sys.stdout.write("\x1b[?25l") # hide cursor
bus.add_signal_receiver(bus_handler, bus_name="org.gnome.Pomodoro")

def exit_handler():
    sys.stdout.write("\x1b[?25h") # show cursor

atexit.register(exit_handler)

loop = GLib.MainLoop()
loop.run()
