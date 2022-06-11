# OctoPrint-Octo4a_battery

**TODO:** This plugin displays the battery level of yout phone running OctoPrint with [Octo4a](https://github.com/feelfreelinux/octo4a)

![Octo4a_battery](images/screenshot_battery_level.png?raw=true) 

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/tobiasgraf/OctoPrint-Octo4a_battery/archive/master.zip

**TODO:** Describe how to install your plugin, if more needs to be done than just installing it via pip or through
the plugin manager.

## Configuration

**TODO:** This plugin simply reads the file battery from the file '/sys/class/power_supply/battery/capacity'. This works on my Phone (Nexus 5). If this does not work for you, you can change the path in the settings.
