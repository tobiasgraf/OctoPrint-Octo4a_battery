/*
 * View model for OctoPrint-Octo4a_battery
 *
 * Author: kame
 * License: AGPLv3
 */
$(function() {
    function Octo4a_batteryViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        self.settings = parameters[0];
        self.batteryLevel = ko.observable(100);
        self.batteryIcon = ko.observable("fas fa-battery-half");


        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its
        // dependencies have already been initialized. It is especially guaranteed that this method
        // gets called _after_ the settings have been retrieved from the OctoPrint backend and thus
        // the SettingsViewModel been properly populated.
        self.onBeforeBinding = function() {
            self.batteryLevel(100);
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            console.log(data);
            if (data.batteryLevel) {
                // Add fahrenheit
                console.log("got battery level");
                self.batteryLevel(data.batteryLevel);
                if ( data.batteryLevel < 10) { self.batteryIcon("fas fa-battery-empty"); }
                // else if ( data.batteryLevel < 25) { self.batteryIcon("fas fa-battery-low"); }
                else if ( data.batteryLevel < 50) { self.batteryIcon("fas fa-battery-quarter"); }
                else if ( data.batteryLevel < 75) { self.batteryIcon("fas fa-battery-half"); }
                else if ( data.batteryLevel < 90) { self.batteryIcon("fas fa-battery-three-quarters"); }
                else { self.batteryIcon("fas fa-battery-full"); }
            }
        };

    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Octo4a_batteryViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_octo4a_battery, #tab_plugin_octo4a_battery, ...
        elements: [ "#navbar_plugin_octo4a_battery" ]
    });
});
