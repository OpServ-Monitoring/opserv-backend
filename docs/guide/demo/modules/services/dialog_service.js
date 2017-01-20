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



            scope.tiles = buildGridModel();

            function buildGridModel() {
                var results = [];
                for (var i=0;i<3;i++){
                    var it={};
                    it.title='title'+i;
                    it.span={row:1,col:1};
                    it.samplingRate = 1000+(1000*i);
                    results.push(it);
                }
                return results;
            }

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
                loginSecret: undefined
            };

            //autologing when secret is already set
            var secret = localStorage.getItem('secret');
            if (secret){
                $scope.isLoading = true;
                submit(secret);
            }

            $scope.cancel = function() {
                $mdDialog.cancel();
            };

            $scope.submit = function() {
                submit($scope.form.loginSecret);
            };

            function submit(secret) {
                if(secret!= ""){
                    prefService.validateUser(secret);
                    $scope.isLoading = true;
                }else{
                    $scope.failedValidation = true;
                }
            }

            $scope.$on(EVENT_USER_VALIDATED,function (event, status) {
                if (status){
                    if ($scope.form.loginSecret){
                        //set secret in local storage, when it is set in $scope.form.loginSecret (by manual login)
                        localStorage.setItem('secret',$scope.form.loginSecret);
                    }
                    authService.setLogin(status);
                    $mdDialog.hide(status);
                }else{
                    $scope.failedValidation = true;
                    toastService.showErrorToast("Uservalidierung Fehlgeschlagen");
                    $scope.isLoading = false;

                }
            });

            $scope.$watch('form.loginSecret',function (newVal, oldVal) {
                if(newVal != undefined){
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

