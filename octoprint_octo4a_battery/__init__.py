# coding=utf-8
from __future__ import absolute_import

from octoprint.util import RepeatedTimer


import octoprint.plugin

class Octo4a_batteryPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin
):

    def __init__(self):
        # Array of raspberry pi SoC's to check against, saves having a large if/then statement later
        self._checkBatteryTimer = None
        self._batteryLevelTmp = 100

    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["batteryLevelPath"]))
        self.start_custom_timer(5)


    def start_custom_timer(self, interval):
        self._checkBatteryTimer = RepeatedTimer(interval, self.update_battery, run_first=True)
        self._checkBatteryTimer.start()


    def update_battery(self):

        try:
            path = self._settings.get(["batteryLevelPath"])
            f = open(path, "r")
            self._batteryLevelTmp = f.read()
        except:
            self._batteryLevelTmp = "invalid path"; 
        # self._batteryLevelTmp -= 1
        batteryStatus = "Full"
        self._logger.debug("match: level: %s" % self._batteryLevelTmp)
        self._plugin_manager.send_plugin_message(self._identifier,
                                                 dict(batteryLevel=self._batteryLevelTmp,batteryStatus=batteryStatus))

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(batteryLevelPath="/sys/class/power_supply/battery/capacity")


    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]
    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/octo4a_battery.js"],
            "css": ["css/octo4a_battery.css"],
            "less": ["less/octo4a_battery.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "octo4a_battery": {
                "displayName": "Octo4a_battery Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "tobiasgraf",
                "repo": "OctoPrint-Octo4a_battery",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/tobiasgraf/OctoPrint-Octo4a_battery/archive/{target_version}.zip",
            }
        }
        


    def get_template_vars(self):
        return dict(batteryLevelPath=self._settings.get(["batteryLevelPath"]))

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Octo4a_battery Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octo4a_batteryPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

