app.factory('dialogService',function($mdDialog){

    var service = {};

    service.showWidgetSettings = function (currentSettings, callback) {
        $mdDialog.show({
            controller: widgetSettingsController,
            templateUrl: 'views/templates/dialog/widget_settings_dialog.html',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true // Only for -xs, -sm breakpoints.
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function widgetSettingsController($scope, $mdDialog){
            $scope.currentMode = currentSettings.currentMode;
            $scope.title = currentSettings.title;
            $scope.modes = currentSettings.modes;
            $scope.samplingRateLive = currentSettings.samplingRateLive;

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                var answer = {};
                answer['newTitle'] = $scope.title;
                answer['newMode'] = $scope.currentMode;
                answer['newSamplingRateLive'] = $scope.samplingRateLive;
                $mdDialog.hide(answer);
            };
        }
    };

    service.showDashboardSettings = function (currentSettings, callback) {
        $mdDialog.show({
            controller: dashboardSettingsController,
            templateUrl: 'views/templates/dialog/dashboard_settings_dialog.html',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true // Only for -xs, -sm breakpoints.
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function dashboardSettingsController($scope, $mdDialog){
            $scope.title = currentSettings.title;
            $scope.baseUrl = currentSettings.baseUrl;

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                var answer = {};
                answer['newTitle'] = $scope.title;
                answer['newBaseUrl'] = $scope.baseUrl;
                $mdDialog.hide(answer);
            };
        }
    };

    service.showOpservSettings = function (callback) {
        $mdDialog.show({
            controller: opservSettingsController,
            templateUrl: 'views/templates/dialog/opserv_settings_dialog.html',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true // Only for -xs, -sm breakpoints.
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function opservSettingsController($scope, $mdDialog){
            var scope = $scope;

            scope.selectedYear = 0;
            scope.years = [];
            scope.items = [];
            var currentYear = new Date().getFullYear();
            var monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
            // Build a list of months over 20 years
            for (var y = currentYear; y >= (currentYear-20); y--) {
                scope.years.push(y);
                scope.items.push({year: y, text: y, header: true});
                for (var m = 11; m >= 0; m--) {
                    scope.items.push({year: y, month: m, text: monthNames[m]});
                }
            }
            // Whenever a different year is selected, scroll to that year
            $scope.$watch('ctrl.selectedYear', angular.bind(this, function(yearIndex) {
                var scrollYear = Math.floor(scope.topIndex / 13);
                if(scrollYear !== yearIndex) {
                    scope.topIndex = yearIndex * 13;
                }
            }));
            // The selected year should follow the year that is at the top of the scroll container
            $scope.$watch('ctrl.topIndex', angular.bind(this, function(topIndex) {
                var scrollYear = Math.floor(topIndex / 13);
                scope.selectedYear = scrollYear;
            }));


            $scope.title = 'TEST';
            $scope.baseUrl = 'BLA';

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                var answer = {};
                $mdDialog.hide(answer);
            };
        }
    };

    return service;
});

