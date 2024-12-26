import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

from driink.notifier import notify
from driink import db
from driink import __version__


class DriinkApplet:

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            "driink-applet",
            os.path.expanduser("~/.local/share/driink/resources/water.png"),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = Gtk.Menu()

        progress_item = Gtk.MenuItem(label="Progress")
        # progress_item.connect("activate", self.open_settings)
        menu.append(progress_item)

        # Menu item to log water consumption
        log_menu = Gtk.Menu()
        log_item = Gtk.MenuItem(label="Log ...")
        log_item.set_submenu(log_menu)

        menu.append(log_item)
        quantities = [
            ("100ml", 100),
            ("250ml", 250),
            ("500ml", 500),("750ml", 750)
        ]
        for label, amount in quantities:
            quantity_item = Gtk.MenuItem(label=label)
            quantity_item.connect("activate", self.log_water, amount)
            log_menu.append(quantity_item)

        settings_item = Gtk.MenuItem(label="Settings")
        settings_item.connect("activate", self.open_settings)
        menu.append(settings_item)

        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self.show_about)
        menu.append(about_item)

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

    def open_settings(self, _):
        print("Open settings clicked!")

    def show_about(self, _):
        """Show the About dialog."""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("Driink - Stay Hydrated")
        dialog.set_version(__version__)
        dialog.set_comments("A simple applet to track water consumption and stay hydrated.")
        dialog.set_website("https://github.com/gaccardo/driink")
        dialog.set_authors(["Guido Accardo"])
        dialog.set_logo_icon_name("dialog-information")  # Use a system icon or set a custom logo

        # Show the dialog
        dialog.run()
        dialog.destroy()

    def show_menu(self, menu):
        """Show the given menu."""
        menu.show_all()
        menu.popup(None, None, None, None, Gdk.CURRENT_TIME, 0)


def main():
    applet = DriinkApplet()
    Gtk.main()

if __name__ == "__main__":
    main()

