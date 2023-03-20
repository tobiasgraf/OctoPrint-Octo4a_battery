# coding=utf-8
from __future__ import absolute_import
import requests

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
        self._batteryLevel = 100
        self._lastWarningSent = 100

    def on_after_startup(self):
        self._logger.info(f'Hello World! (more: {self._settings.get(["batteryLevelPath"])}, "telegram enabled: {self._settings.get(["telegramEnabled"])}')
        self.start_custom_timer(5)


    def start_custom_timer(self, interval):
        self._checkBatteryTimer = RepeatedTimer(interval, self.update_battery, run_first=True)
        self._checkBatteryTimer.start()

    def check_warning_threshold(self, newValue):
        if self._settings.get(["telegramEnabled"]) == False:
            return
        self._logger.debug("\n\ncheck_warning_threshold %s", newValue)
        thresholdHit = 0
        alarmThresholds = [ 5, 15, 25, 35 ]
        for threshold in alarmThresholds:
            if int(newValue) < threshold:
                self._logger.debug("threshold hit %s", threshold)
                thresholdHit = 1
                if self._lastWarningSent <= threshold:
                    self._logger.debug("self._lastWarningSent %i <= threshold: %i" , self._lastWarningSent, threshold)
                    continue
                self.send_telegram_alarm(newValue,threshold)
                self._logger.debug("send_telegram_alarm: %i" ,threshold)
                self._lastWarningSent = threshold
                break
            if int(newValue) >= self._lastWarningSent:
                # the new value is above the last hit threshold ... battery level is rising?
                self._logger.debug("int(newValue) %s > self._lastWarningSent %i" , newValue, self._lastWarningSent)
                self._lastWarningSent = threshold+1
        if thresholdHit == 0:
            # threshold no longer hit ... this must mean the battery level is back up, reset warnings
            self._lastWarningSent = 100
            self._logger.debug("thresholdHit == 0:" )
    

    def send_telegram_alarm(self, value, threshold):
        url = f'https://api.telegram.org/bot{self._settings.get(["telegramBotToken"])}/sendMessage'
        myobj = {'chat_id':self._settings.get(["telegramChatID"]),'text':f'🚨Warning🚨 Battery Level is below { threshold}% (Battery Level: {value}%)'}

        x = requests.post(url, json = myobj)

    def update_battery(self):

        try:
            path = self._settings.get(["batteryLevelPath"])
            f = open(path, "r")
            self._batteryLevel = f.read().strip()
        except:
            self._batteryLevel = "invalid path"; 
        # self._batteryLevelTmp -= 1
        batteryStatus = "Full"
        self._logger.debug("match: level: %s" % self._batteryLevel)
        self._plugin_manager.send_plugin_message(self._identifier,
                                                 dict(batteryLevel=self._batteryLevel,batteryStatus=batteryStatus))
        self.check_warning_threshold(self._batteryLevel)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(batteryLevelPath="/sys/class/power_supply/battery/capacity", telegramBotToken="Token" , telegramChatID="chatID", telegramEnabled = 0)


    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=True),
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
        return dict(batteryLevelPath=self._settings.get(["batteryLevelPath"]),
                    telegramBotToken=self._settings.get(["telegramBotToken"]),
                    telegramChatID=self._settings.get(["telegramChatID"]),
                    telegramEnabled=self._settings.get(["telegramEnabled"]))

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

