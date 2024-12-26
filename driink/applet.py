import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3
from datetime import datetime, date

from driink.notifier import notify
from driink import db
from driink import __version__
import driink.config as u_config
from driink.visualizations import display_progress


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
        progress_item.connect("activate", self.open_progress)
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

    def display_progress_bar(self, total, daily_goal, percentage):
        """Display the progress in a GTK window with a progress bar."""
        # Create a new window
        window = Gtk.Window(title="Water Consumption Progress")
        window.set_default_size(300, 150)
        window.set_resizable(False)

        # Create a vertical box to hold widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)

        # Create a label to display the progress details
        label = Gtk.Label(label=f"Today you've drank: {total} ml\n"
                                f"Daily Goal: {daily_goal} ml\n"
                                f"Progress: {percentage:.2f}%")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(label, False, False, 0)

        # Create a progress bar
        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(percentage / 100)  # Fraction must be between 0 and 1
        progress_bar.set_text(f"{total} ml / {daily_goal} ml")
        progress_bar.set_show_text(True)
        vbox.pack_start(progress_bar, False, False, 0)

        # Add a close button
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", lambda _: window.destroy())
        vbox.pack_start(close_button, False, False, 0)

        # Add the box to the window and show everything
        window.add(vbox)
        window.show_all()

    def open_progress(self, _):
        # Start of today
        start_of_today = datetime.combine(date.today(), datetime.min.time())

        # End of today
        end_of_today = datetime.combine(date.today(), datetime.max.time())

        # Get water consumption from today
        drink_registry = db.get_water_log(start_of_today, end_of_today)
        total = sum(record.amount for record in drink_registry)

        conf = u_config.load_user_config()
        daily_goal = int(conf.get('driink', 'daily_goal'))
        percentage = float(total)*100/float(daily_goal)

        self.display_progress_bar(total, daily_goal, percentage)

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

