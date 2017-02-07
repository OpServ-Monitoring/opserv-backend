app.factory('dialogService',function($mdDialog, prefService, toastService, authService){

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
            $scope.samplingRate = currentSettings.samplingRate;

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                var answer = {};
                answer['newTitle'] = $scope.title;
                answer['newMode'] = $scope.currentMode;
                answer['newSamplingRate'] = $scope.samplingRate;
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

        function dashboardSettingsController($scope, $rootScope, $mdDialog){
            $scope.title = currentSettings.title;
            $scope.baseUrl = currentSettings.baseUrl;
            $scope.isMock = $rootScope.isMock;

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

            scope.rates = [
                {title:"CPU-0-USAGE",samplingRate:2000},
                {title:"NETWORK-NETWORKNAME-TRANSMITTPERSEC",samplingRate:4000},
                {title:"NETWORK-NETWORKNAME-TRANSMITTPERSEC",samplingRate:4000},
                {title:"NETWORK-NETWORKNAME-TRANSMITTPERSEC",samplingRate:4000},
                {title:"NETWORK-NETWORKNAME-TRANSMITTPERSEC",samplingRate:4000},
                {title:"NETWORK-NETWORKNAME-TRANSMITTPERSEC",samplingRate:4000}
            ];

            scope.cancel = function() {
                $mdDialog.cancel();
            };

            scope.submit = function() {
                var answer = {};
                $mdDialog.hide(answer);
            };
        }
    };

    service.showLanguageDialog = function (currentLanguageKey,callback) {
        $mdDialog.show({
            controller: languageController,
            templateUrl: 'views/templates/dialog/language_dialog.html',
            parent: angular.element(document.body),
            clickOutsideToClose: true
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function languageController($rootScope, $scope, $mdDialog){
            $scope.languages = $rootScope.languages;
            $scope.selectedLanguageKey = currentLanguageKey;
            console.log($scope.selectedLanguageKey);

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                $mdDialog.hide($scope.selectedLanguageKey);
            };
        }
    };

    service.showLoginDialog = function (callback) {
        $mdDialog.show({
            controller: loginController,
            templateUrl: 'views/templates/dialog/login_dialog.html',
            parent: angular.element(document.body)
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function loginController($scope, $mdDialog){

            $scope.isLoading = false;
            $scope.failedValidation = false;
            $scope.loginDisabeled = true;
            $scope.form = {
                password: undefined,
                userName: undefined
            };

            //autologing when secret is already set
            var password = localStorage.getItem('password');
            var userName = localStorage.getItem('userName');
            if (password && userName){
                $scope.isLoading = true;
                submit(userName,password);
            }

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                submit($scope.form.userName,$scope.form.password);
            };

            function submit(userName,password) {
                if(password!= "" && userName != ""){
                    prefService.validateUser(userName,password);
                    $scope.isLoading = true;
                }else{
                    $scope.failedValidation = true;
                }
            }

            $scope.$on(EVENT_USER_VALIDATED,function (event, status) {
                if (status){
                    if ($scope.form.password && $scope.form.userName){
                        //set secret in local storage, when it is set in $scope.form.loginSecret (by manual login)
                        localStorage.setItem('password',$scope.form.password);
                        localStorage.setItem('userName',$scope.form.userName);
                    }
                    authService.setLogin(status);
                    $mdDialog.hide(status);
                }else{
                    $scope.failedValidation = true;
                    toastService.showErrorToast("Uservalidierung Fehlgeschlagen");
                    $scope.isLoading = false;

                }
            });

            $scope.$watch('form.password',function (newVal, oldVal) {
                if(newVal != undefined && $scope.form.userName != undefined){
                    $scope.loginDisabeled = false;
                }
                if(newVal == undefined){
                    $scope.loginDisabeled = true;
                }
            });

            $scope.$watch('form.userName',function (newVal, oldVal) {
                if(newVal != undefined && $scope.form.password != undefined){
                    $scope.loginDisabeled = false;
                }
                if(newVal == undefined){
                    $scope.loginDisabeled = true;
                }
            })
        }
    };

    return service;
});

