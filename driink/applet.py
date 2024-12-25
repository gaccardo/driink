import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

from driink.notifier import notify
from driink import db


class DriinkApplet:

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "driink-applet",
            "dialog-information",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        resources_path = os.path.expanduser('~/.local/share/driink/resources')
        self.indicator.set_icon(os.path.join(resources_path, "water.png"))
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = Gtk.Menu()

        # Menu item to log water consumption
        log_item = Gtk.MenuItem(label="Drink 100 ml")
        log_item.connect("activate", self.log_water)
        menu.append(log_item)

        # Menu item to quit the app
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def log_water(self, _):
        db.log_drink(100)
        msg = f"Logged 100ml of water."
        notify(msg)

    def quit(self, _):
        Gtk.main_quit()


def main():
    applet = DriinkApplet()
    Gtk.main()

if __name__ == "__main__":
    main()

