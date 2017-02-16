app.factory('dialogService',function($mdDialog, prefService, toastService, authService, dataService){

    //TODO encoding bei url relevaten encodings einfügen

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

    service.showGatheringRatesSettings = function (dashboardIndex, baseURL, callback) {
        $mdDialog.show({
            controller: gatheringRatesSettingsController,
            templateUrl: 'views/templates/dialog/gathering_rates_settings_dialog.html',
            parent: angular.element(document.body),
            clickOutsideToClose: true,
            fullscreen: true // Only for -xs, -sm breakpoints.
        }).then(function(answer) {
            callback(answer)
        }, function() {});

        function gatheringRatesSettingsController($scope, $mdDialog){
            var scope = $scope;

            scope.rates = [];
            scope.possibleRates=[];
            scope.newRate = {};
            scope.rateforRollback ={};

            dataService.getGatheringRates(baseURL);

            scope.$on(EVENT_ALL_GATHERING_RATES_RECEIVED, function (event, status, gathering_rates) {
                if(status){
                    for (var i=0; i < gathering_rates.length; i++){
                        var object = gathering_rates[i];
                        if(object.metric != "info" && object.component_type !="system"){
                            object.oldGatheringRate = object.gathering_rate; // security-store for rollback
                            if (object.gathering_rate != 0){
                                if(object.component_arg != null){
                                    object.title = object.component_type+"-"+object.component_arg+"-"+object.metric;
                                    scope.rates.push(object)
                                }else{
                                    object.title = object.component_type+"-"+object.metric;
                                    scope.rates.push(object)
                                }
                            }else{

                                if(object.component_arg != null){
                                    object.title = object.component_type+"-"+object.component_arg+"-"+object.metric;
                                    scope.possibleRates.push(object);
                                }else{
                                    object.title = object.component_type+"-"+object.metric;
                                    scope.possibleRates.push(object);
                                }

                            }
                        }
                    }
                    sortRates();
                    sortPossibleRates();
                }else{
                    toastService.showErrorToast("Fehler beim Laden der Gathering-Rates")
                }
            });

            scope.$on(EVENT_SET_GATHERING_RATE, function (event, status, gatheringRateObject) {
                var index = 0;
                if(status){
                    if(gatheringRateObject.gathering_rate != 0){
                        //include added rate in view
                        scope.rates.push(gatheringRateObject);
                        sortRates();
                        //exclude from possible Rate
                        index = scope.possibleRates.indexOf(gatheringRateObject);
                        scope.possibleRates.splice(index,1);
                    }else{
                        //exclude deleted rate from view
                        index = scope.rates.indexOf(gatheringRateObject);
                        scope.rates.splice(index,1);
                        // put in possibleRates
                        scope.possibleRates.push(gatheringRateObject);
                        sortPossibleRates();
                        toastService.showRollbackToast("gathering rate", function (doRollback) {
                            if(doRollback){
                                index = scope.possibleRates.indexOf(gatheringRateObject);
                                scope.possibleRates.splice(index,1);
                                gatheringRateObject.gathering_rate = gatheringRateObject.oldGatheringRate;
                                scope.rates.push(gatheringRateObject);
                                sortRates();
                            }
                        })
                    }
                }else{
                    toastService.showErrorToast("Fehler beim Speichern der Gathering Rate");
                }
            });

            scope.$on(EVENT_UPDATE_GATHERING_RATE, function (event, success, updatedRateObject) {
                var index =0;
                if (success){
                    index = scope.rates.indexOf(updatedRateObject);
                    scope.rates[index].oldGatheringRate = updatedRateObject.gathering_rate;
                }else{
                    index = scope.rates.indexOf(updatedRateObject);
                    scope.rates[index].gathering_rate = updatedRateObject.oldGatheringRate;
                    toastService.showErrorToast("Update der Rate fehlgeschlagen")
                }
            });

            scope.$on(EVENT_SLIDER_DRAG_END, function (event, ariaLabel, index) {
                if(ariaLabel == "gathering_rate"){
                    var changedRateObject = scope.rates[index];
                    var component = getComponent(changedRateObject.component_type);
                    dataService.updateGatheringRate(baseURL, component, changedRateObject.component_arg, changedRateObject.metric, changedRateObject)
                }
            });

            scope.$watch('newRate',function (newVal, oldVal) {
                if (newVal.component_type){
                    var newRateObject = scope.newRate;
                    newRateObject.gathering_rate = 1000;
                    var component = getComponent(newRateObject.component_type);
                    dataService.setGatheringRate(baseURL, component, newRateObject.component_type, newRateObject.metric, newRateObject);
                }
            });

            scope.deleteRate = function (rateToDeleteObject) {
                rateToDeleteObject.gathering_rate = 0;
                var component = getComponent(rateToDeleteObject.component_type);
                dataService.setGatheringRate(baseURL, component, rateToDeleteObject.component_arg, rateToDeleteObject.metric, rateToDeleteObject);
            };

            scope.cancel = function() {
                $mdDialog.cancel();
            };

            function sortRates() {
                scope.rates.sort(function (a, b) {
                    var textA = a.title.toUpperCase();
                    var textB = b.title.toUpperCase();
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                });
            }

            function sortPossibleRates() {
                scope.possibleRates.sort(function (a, b) {
                    var textA = a.title.toUpperCase();
                    var textB = b.title.toUpperCase();
                    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
                })
            }

            function getComponent(component_type) {
                switch (component_type){
                    case "cpu":
                        return "cpus";
                        break;
                    case "cpucore":
                        return "cpu-cores";
                        break;
                    case "network":
                        return "networks";
                        break;
                    case "partition":
                        return "partitions";
                        break;
                    case "gpu":
                        return "gpus";
                        break;
                    case "disk":
                        return "disks";
                        break;
                    case "memory":
                        return "memory";
                        break;
                }
            }
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
                    //save in localstorage for http interceptor
                    localStorage.setItem('password',password);
                    localStorage.setItem('userName',userName);
                    prefService.validateUser(userName,password);
                    $scope.isLoading = true;
                }else{
                    $scope.failedValidation = true;
                }
            }

            $scope.$on(EVENT_USER_VALIDATED,function (event, status) {
                if (status){
                    authService.setLogin(status);
                    $mdDialog.hide(status);
                }else{
                    // delete from localstorage if login failed
                    localStorage.removeItem('password');
                    localStorage.removeItem('userName');
                    $scope.failedValidation = true;
                    toastService.showErrorToast("Uservalidierung Fehlgeschlagen");
                    $scope.isLoading = false;

                }
            });

            // $scope.$watch('form.password',function (newVal, oldVal) {
            //     if(newVal != undefined && $scope.form.userName != undefined){
            //         $scope.loginDisabeled = false;
            //     }
            //     if(newVal == undefined){
            //         $scope.loginDisabeled = true;
            //     }
            // });

            $scope.$watch('form.userName',function (newVal, oldVal) {
                // if(newVal != undefined && $scope.form.password != undefined){
                //     $scope.loginDisabeled = false;
                // }
                if(newVal != undefined ){
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

