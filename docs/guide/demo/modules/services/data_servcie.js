/**
 * Created by Snare on 29.08.16.
 */

app.factory('dataService',function($http, $rootScope, toastService,$timeout){

//------------------------------------------------ Variables --------------------------------------------------------------------------------------------------------------------------------------//
    var service = {
        dashboards: [],
        intervalMap: {}
    };

//------------------------------------------------ Load Metrics --------------------------------------------------------------------------------------------------------------------------------------//

    const CURRENT_API_PATH = '/api/data/current';
    const REALTIME_QUERY_STRING = '?realtime=true';
    const HISTORY_START_STRING = '?start=';
    const HISTORY_END_STRING_MUST_BE_LAST = '&end=';

    service.enableCILiveTimer = function(baseUrl, ci, id, category, samplingRate){
        var intervalName = baseUrl+ci+id+category;
        if(!intervalExists(intervalName)){
            createCiLiveInterval(baseUrl, ci, id, category, samplingRate, intervalName);
        }else{
            increaseIntervalUsedBy(intervalName);
            service.updateSamplingRateOfCiLiveTimer(baseUrl, ci, id, category, samplingRate)
        }
    };

    service.disableCiLiveTimer = function(baseUrl, ci, id, category){
        var intervalName = baseUrl+ci+id+category;
        disableInterval(intervalName, baseUrl);
    };

    service.updateSamplingRateOfCiLiveTimer = function(baseUrl, ci, id, category, newSamplingRate){
        var intervalName = baseUrl+ci+id+category;
        if(intervalExists(intervalName)){
            var currentUsedBy = service.intervalMap[intervalName].usedBy;
            stopAndDeleteInterval(intervalName);
            createCiLiveInterval(baseUrl, ci, id, category, newSamplingRate, intervalName, function (success, response) {
                if (success){
                    updateIntervalUsedBy(intervalName,currentUsedBy);

                }else{
                    toastService.showErrorToast("Fehler beim Samplingrate setzten")// todo sprache anpassen
                }
            });

        }
    };

    service.getCiHistoryData = function(baseUrl, ci, id, category, start, end){
        var urls = buildUrls(baseUrl,ci,id,category, false, start, end);
        console.log("url: ",urls.forData);
        $http.get(urls.forData).then(function successCallback(response) {
            var parsed_values = parseHistoryValues(response.data.data.values);
            $rootScope.$broadcast(EVENT_CI_HISTORY_DATA_RECEIVED, true, baseUrl, ci, id, category, start, end, parsed_values);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_CI_HISTORY_DATA_RECEIVED, false, baseUrl, ci, id, category, start, end, null);
        });
    };

    service.updateAllBaseUrlRelatedIntervals = function (oldBaseUrl, newBaseUrl, widgets){
        var intervalValues = {};
        var newIntervalName = "";
        var count = 0;
        for (var intervalName in service.intervalMap){
            if (service.intervalMap.hasOwnProperty(intervalName)){
                if (service.intervalMap[intervalName].baseUrl == oldBaseUrl){
                    intervalValues = service.intervalMap[intervalName];
                    stopAndDeleteInterval(intervalName);
                    newIntervalName = newBaseUrl+intervalValues.ci+intervalValues.id+intervalValues.category;
                    createCiLiveInterval(newBaseUrl,intervalValues.ci,intervalValues.id,intervalValues.category,intervalValues.samplingRate, newIntervalName, intervalValues.usedBy);
                    count ++;
                }
            }
        }
        if (count != widgets.length){
            createIntervalsForWidgets(widgets, newBaseUrl)
        }
    };

    service.getSamplingRateForCi = function (baseUrl, ci, id, cat) {
        var url="";
        if (id){
            url = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+id+'/'+cat;
        }else{
            url = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+cat;
        }
        $http.get(url).then(function successCallback(response) {
            $rootScope.$broadcast(EVENT_GATHERING_RATE_RECEIVED, true, baseUrl, ci, id, cat, response.data.data.gathering_rate);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_GATHERING_RATE_RECEIVED, false, baseUrl, ci, id, cat, undefined);
        });

    };

//------------------------------------------------ CI Info --------------------------------------------------------------------------------------------------------------------------------------//

    service.getCIs = function (baseUrl) {
        return $http.get(baseUrl+CURRENT_API_PATH).then(function successCallback(response) {
            var cis = getValuesFromChildrenLinks(response.data.links.children);

            $timeout(function() {
                $rootScope.$broadcast(EVENT_CIS_RECEIVED, true, cis);
            }, 3000);


        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_CIS_RECEIVED, false, response);
        });
    };

    service.getCiIds = function(ciName, baseUrl){
        return $http.get(baseUrl+CURRENT_API_PATH+'/'+ciName).then(function successCallback(response) {
            var ids = getValuesFromChildrenLinks(response.data.links.children);
            $rootScope.$broadcast(EVENT_CI_IDS_RECEIVED, true, ciName, ids);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_CI_IDS_RECEIVED, false, response);
        });
    };

    service.getCiCats = function(ciName, ciId, baseUrl){
        return $http.get(baseUrl+CURRENT_API_PATH+'/'+ciName+'/'+ciId).then(function successCallback(response) {
            var cats = getValuesFromChildrenLinks(response.data.links.children);
            $rootScope.$broadcast(EVENT_CI_CATS_RECEIVED, true, ciName, cats);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_CI_CATS_RECEIVED, false, response);
        });
        // return $http.get(baseUrl+CURRENT_API_PATH+'/'+ciName+'/'+encodeURIComponent(ciId)).then(function successCallback(response) {
        //     var cats = getValuesFromChildrenLinks(response.data.links.children);
        //     $rootScope.$broadcast(EVENT_CI_CATS_RECEIVED, true, ciName, cats);
        // }, function errorCallback(response) {
        //     $rootScope.$broadcast(EVENT_CI_CATS_RECEIVED, false, response);
        // });
    };

    service.getMemoryCats = function (ciName, baseUrl) {
        return $http.get(baseUrl+CURRENT_API_PATH+'/'+ciName).then(function successCallback(response) {
            var cats = getValuesFromChildrenLinks(response.data.links.children);
            $rootScope.$broadcast(EVENT_MEMORY_CATS_RECEIVED, true, ciName, cats);
        }, function errorCallback(response) {
            $rootScope.$broadcast(EVENT_MEMORY_CATS_RECEIVED, false, response);
        });
    };

//------------------------------------------------ Helper --------------------------------------------------------------------------------------------------------------------------------------//

    function createCiLiveInterval(baseUrl, ci, id, category, samplingRate, intervalName, callback){
        var urls = buildUrls(baseUrl, ci, id, category,true);
        setSamplingRate(urls.forSamplingRate,samplingRate,function (success) {
            if (success){
                try {
                    var liveInterval = setInterval(function () {
                        $http.get(urls.forData).then(function successCallback(response) {
                            $rootScope.$broadcast(EVENT_CI_LIVE_DATA_RECEIVED, true, baseUrl, ci, id, category, response.data.data);
                        }, function errorCallback(response) {
                            $rootScope.$broadcast(EVENT_CI_LIVE_DATA_RECEIVED, false, baseUrl, ci, id, category, undefined);
                        });
                    }, samplingRate);
                    addIntervalToMap(intervalName, liveInterval, baseUrl, ci, id, category, samplingRate);
                    if (callback && typeof callback == "function"){
                        callback(true)
                    }
                }catch (error) {
                    if (callback && typeof callback == "function"){
                        callback(false);
                    }
                    $rootScope.$broadcast(EVENT_CI_LIVE_DATA_RECEIVED, false, baseUrl, ci, id, category, undefined);
                }
            }else{
                if (callback && typeof callback == "function"){
                    callback(false);
                }
                $rootScope.$broadcast(EVENT_CI_LIVE_DATA_RECEIVED, false, baseUrl, ci, id, category, undefined);
            }

        });
    }

    function createIntervalsForWidgets(widgets, baseUrl) {
        var intervalName;
        widgets.forEach(function (widget) {
            var displayItem = widget.displayItem;
            intervalName = baseUrl+displayItem.ci+displayItem.id+displayItem.category;
            if (!intervalExists(intervalName)){
                createCiLiveInterval(baseUrl, displayItem.ci, displayItem.id, displayItem.category, displayItem.samplingRate, intervalName);
            }
        });
    }

    function setSamplingRate(url, samplingRate, callback) {
        $http.put(url,{gathering_rate:samplingRate}).then(function onSuccess(response) {
            callback(true);
        }, function onError(response) {
            callback(false);
        });
    }

    function parseHistoryValues(values) {
        var minArray=[];
        var maxArray=[];
        var avgArray=[];

        angular.forEach(values,function (object) {
            minArray.push([object.timestamp, object.min]);
            maxArray.push([object.timestamp, object.max]);
            avgArray.push([object.timestamp, object.avg])
        });

        return [{name:"min-values",data:minArray},{name:"avg-values",color:"#d966ff",data:avgArray},{name:"max-values",color:"#ff471a",data:maxArray}]
    }

    function addIntervalToMap(intervalName, liveInterval, baseUrl, ci, id, category, samplingRate) {
        var intervalValues = {
            interval: liveInterval,
            baseUrl: baseUrl,
            ci: ci,
            id: id,
            category: category,
            samplingRate: samplingRate,
            usedBy: 1
        };
        service.intervalMap[intervalName] = intervalValues;
    }

    function disableInterval(intervalName) {
        if (intervalExists(intervalName)) {
            decreaseIntervalUsedByCounter(intervalName);
            if (service.intervalMap[intervalName].usedBy == 0) {
                stopAndDeleteInterval(intervalName);
            }
        }
    }

    function intervalExists(intervalName) {
        return !!service.intervalMap[intervalName];
    }

    function stopAndDeleteInterval(intervalName) {
        var interval = service.intervalMap[intervalName].interval;
        clearInterval(interval);
        delete service.intervalMap[intervalName];
    }

    function updateIntervalUsedBy(intervalName, countCurrentIntervals ) {
        service.intervalMap[intervalName].usedBy = countCurrentIntervals;
    }

    function increaseIntervalUsedBy(intervalName) {
        service.intervalMap[intervalName].usedBy = service.intervalMap[intervalName].usedBy + 1;
    }

    function decreaseIntervalUsedByCounter(intervalName) {
        service.intervalMap[intervalName].usedBy = service.intervalMap[intervalName].usedBy - 1;
    }

    function buildUrls(baseUrl, ci, id, cat, isLive, historyStartTime, historyEndTime) {
        var urls = {forSamplingRate:'',forData:''};
        console.log("id: ",id);
        if(id != undefined){
            urls.forSamplingRate = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+id+'/'+cat;
            if(isLive){
                urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+id+'/'+cat+REALTIME_QUERY_STRING;
                return urls;
            }else{
                // urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+id+'/'+cat+HISTORY_START_STRING+historyStartTime+HISTORY_END_STRING_MUST_BE_LAST+historyEndTime;
                // return urls;
                urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+id+'/'+cat;
                return urls;
            }
        }else{
            urls.forSamplingRate = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+cat;
            if(isLive){
                urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+cat+REALTIME_QUERY_STRING;
                return urls;
            }else{
                // urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+cat+HISTORY_START_STRING+historyStartTime+HISTORY_END_STRING_MUST_BE_LAST+historyEndTime;
                // return urls;
                urls.forData = baseUrl+CURRENT_API_PATH+'/'+ci+'/'+cat;
                return urls;
            }
        }
    }

    function getValuesFromChildrenLinks(childrenLinks) {
        var ids =[];
        if (childrenLinks){
            angular.forEach(childrenLinks,function (link) {
                var childrenAdress = link.href;
                var cutInArray = childrenAdress.split("/");
                var lastItem = cutInArray[cutInArray.length-1];
                ids.push(lastItem);
            });
            return ids;
        }else{
            return [];
        }
        // var ids =[];
        // if (childrenLinks){
        //     angular.forEach(childrenLinks,function (link) {
        //         var childrenAdress = link.href;
        //         var cutInArray = childrenAdress.split("/");
        //         var lastItem = cutInArray[cutInArray.length-1];
        //         ids.push(decodeURIComponent(lastItem));
        //     });
        //     return ids;
        // }else{
        //     return [];
        // }
    }

    return service;
});


//$timeout(function() {
//    otherService.updateTestService('Mellow Yellow')
//    console.log('update with timeout fired')
//}, 3000);