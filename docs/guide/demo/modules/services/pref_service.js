
app.factory('prefService',function($http, $rootScope, $timeout){

//------------------------------------------------Variablen--------------------------------------------------------------------------------------------------------------------------------------//
    var service = {};

//------------------------------------------------ Dashboards --------------------------------------------------------------------------------------------------------------------------------------//

    /**
     * läd alle Dashobards eines Users
     * @returns {*}
     */
    service.getDashboards = function(){
        return $http.get('/api/preferences/v1/dashboards').then(function successCallback(response) {
            // var standardItemsOne = [
            //     { id: 0, sizeX: 15, sizeY: 10, row: 0, col: 0, displayItem: {ci: 'cpus', id: 0, category: 'usage', title:"CPUS 0 USAGE ", displayAsChart:true, realtime:true, samplingRate:1000}},
            //     { id: 1, sizeX: 15, sizeY: 10, row: 0, col: 15, displayItem: {ci: 'cpu-cores', id: 0, category: 'usage', title:"CPU-CORES 0 USAGE", displayAsChart:true, realtime:true, samplingRate:1000}},
            //     { id: 2, sizeX: 15, sizeY: 10, row: 10, col: 10, displayItem: {ci: 'cpu-cores', id: 1, category: 'usage', title:"CPU-CORES 1 USAGE", displayAsChart:true, realtime:true, samplingRate:1000}}
            //     //{ id: 2, sizeX: 2, sizeY: 1, row: 0, col: 4, displayItem: {type: 'text', config:{}} },
            //     //{ id: 3, sizeX: 2, sizeY: 1, row: 1, col: 0, displayItem: {type: 'text', config:{}} },
            //     //{ id: 4, sizeX: 2, sizeY: 2, row: 1, col: 4, displayItem: {type: 'text', config:{}} },
            //     //{ id: 1, sizeX: 3, sizeY: 3, row: 27, col: 0, displayItem: {type: 'text', config:{}} }
            // ];
            //
            // var dashboards=[
            //     { title: 'Default Monitor',widgets:standardItemsOne, baseUrl: 'http://localhost:4000'} // https://397b6935.ngrok.io
            // ];

            $rootScope.$broadcast(EVENT_DASHBOARDS_RECEIVED, true, response.data.data.value);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_DASHBOARDS_RECEIVED, false, null);
        });
    };

    /**
     * speichert alles dashboards
     * @param dashboards
     * @returns {*}
     */
    service.saveDashboards = function(dashboards){
        return $http.put('/api/preferences/v1/dashboards',{value:dashboards}).then(function successCallback(response) {
            $rootScope.$broadcast(EVENT_DASHBOARDS_SAVED, true);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_DASHBOARDS_SAVED, false);
        });
    };

    service.validateUser = function (loginSecret) {
        if (loginSecret == 'opserv'){
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