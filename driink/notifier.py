import notify2
from dynaconf import settings


def notify(message):
    # Initialize the notification system
    notify2.init("Water Tracker")

    # Create a notification object
    n = notify2.Notification("Driink - Stay Hydrated!", message)

    # Set urgency level (optional)
    n.set_urgency(notify2.URGENCY_NORMAL)

    # Set timeout in milliseconds (optional)
    n.set_timeout(settings.NOTIFICATION_TIMEOUT)

    # Show the notification
    n.show()
