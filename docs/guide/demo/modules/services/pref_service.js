
app.factory('prefService',function($http, $rootScope, $timeout){

//------------------------------------------------ Variables --------------------------------------------------------------------------------------------------------------------------------------//
    var service = {};

//------------------------------------------------ Dashboards --------------------------------------------------------------------------------------------------------------------------------------//

    service.getDashboards = function(){
        var url = "";
        if ($rootScope.isMock){
            url = "/mock/api/dashboards"
        }else{
            url = '/api/preferences/v1/dashboards'
        }
        return $http.get(url).then(function successCallback(response) {
            var dashboards= [];
            if(response.data.data.value){
                dashboards = response.data.data.value;
            }else{
                var defaultWidgets = [
                    { id: 0, sizeX: 15, sizeY: 10, row: 0, col: 0, displayItem: {ci: 'cpus', id: 0, category: 'usage', title:"CPUS 0 USAGE ", displayAsChart:true, realtime:true, samplingRate:1000}}
                ];
                dashboards=[
                    { title: 'Default Monitor',widgets:defaultWidgets, baseUrl: 'http://localhost:31337'} // https://397b6935.ngrok.io
                ];
            }
            $rootScope.$broadcast(EVENT_DASHBOARDS_RECEIVED, true, dashboards);
        }, function errorCallback(response) {
            //TODO beim Error trotzdem default mitgeben oder alle funktionen ausblenden?
            $rootScope.$broadcast(EVENT_DASHBOARDS_RECEIVED, false, undefined);
        });
    };

    service.saveDashboards = function(dashboards){
        if ($rootScope.isMock){
            // emulate save is successfull
            $rootScope.$broadcast(EVENT_DASHBOARDS_SAVED, true);
        }else{
            var url = '/api/preferences/v1/dashboards';
            return $http.put(url,{value:dashboards}).then(function successCallback(response) {
                $rootScope.$broadcast(EVENT_DASHBOARDS_SAVED, true);
            }, function errorCallback(response) {
                $rootScope.$broadcast(EVENT_DASHBOARDS_SAVED, false);
            });
        }

    };

    service.validateUser = function (userName, password) {
        if (userName == 'opserv' && password=="test"){
            $timeout(function() {
                $rootScope.$broadcast(EVENT_USER_VALIDATED, true);
            }, 500);
        }else{
            $timeout(function() {
                $rootScope.$broadcast(EVENT_USER_VALIDATED, false);
            }, 500);
        }


        // return $http.put('',{loginSecret:loginSecret}).then(function successCallback(response) {
        //     $rootScope.$broadcast(EVENT_USER_VALIDATED, true);
        // }, function errorCallback(response) {
        //     $rootScope.$broadcast(EVENT_USER_VALIDATED, false);
        // });
    };

    return service;
});


// $timeout(function() {
//    otherService.updateTestService('Mellow Yellow')
//    console.log('update with timeout fired')
// }, 3000);