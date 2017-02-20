/**
 * Created by Snare on 25.08.16.
 */
app.directive('ktDashboardWidget',[ 'dataService',function (dataService) {
    return {
        restrict: 'E',
        templateUrl: 'views/templates/widgets/kt_dashboard_widget.html',
        scope: {
            baseurl: '=',
            widgetindex: '=',
            dashboardindex: '=',
            displayitem: '='
        },
        controller: ['$scope','dialogService', '$rootScope', 'toastService', function WidgetController($scope,dialogService,$rootScope,toastService) {
            //-------------------------- variables -------------------------------------------------------------------------

            var scope = $scope;
            var rootScope = $rootScope;

            scope.samplingRate = 0;
            scope.currentMode = {};

            getSamplingRateForCi(scope.baseurl,scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category);

            scope.modes =[
                {text:"Live"},
                {text:"History"}
            ];

            scope.displayAsChart = scope.displayitem.displayAsChart;

            scope.defaultHistorieStartValue=0;
            scope.defaultHistorieEndValue=0;

            scope.isEditing = rootScope.isEditMode;

            scope.config = {
                options: {
                    chart: {
                        zoomType: 'x',
                        animation: true,
                        events: {
                            load: function () {
                                toggleVisibilityHighchartsButtons(rootScope.isEditMode);
                                scope.chart.reflow()
                            }
                        }
                    },
                    rangeSelector: {
                        labelStyle: {
                            display: 'none'
                        },
                        buttonTheme: { // styles for the buttons
                            fill: 'none',
                            style: {
                                fontWeight: 'bold'
                            },
                            states :{
                                hover:{
                                    fill:'none'
                                },
                                select:{
                                    fill:'none',
                                    style:{
                                        color:'#00b8d4'
                                    }
                                },
                                disabled:{
                                    style:{
                                        color :'#444444'
                                    }
                                }
                            }
                        },
                        buttonSpacing:10,
                        buttons: [{
                            count: 20,
                            type: 'second',
                            text: '30s'
                        }, {
                            count: 40,
                            type: 'second',
                            text: '40s'
                        }, {
                            type: 'all',
                            text: 'All'
                        }],
                        inputEnabled: false
                        //selected: 0,
                        //enabled: true
                    },
                    navigator: {
                        enabled: true
                    },
                    navigation:{
                        buttonOptions: {
                            theme: {
                                states: {
                                    hover: {
                                        fill: 'rgb(80, 80, 83)',
                                        stroke: 'rgba(255,255,255,0.87)',
                                        style:{
                                            color: '#000'
                                        }
                                    },
                                    select: {
                                        stroke: 'rgba(255,255,255,0.87)',
                                        fill: 'rgba(255,255,255,0.2)'
                                    }
                                }
                            }
                        },
                        menuStyle: {
                            background: '#242424',
                            'box-shadow': '0px 0px 0px #fff',
                            'border-color': '#242424'
                        },
                        menuItemStyle: {
                            color: 'rgba(255,255,255,0.87)',
                            'font-family': '"Roboto", "Helvetica", "Arial", sans-serif'
                        },
                        menuItemHoverStyle: {
                            background: 'rgba(255,255,255,0.2)'
                        }
                    },
                    loading: {
                        style: {
                            backgroundColor: 'silver'
                        },
                        labelStyle: {
                            color: 'black'
                        }
                    },
                    tooltip:{
                        enabled:false
                    },
                    xAxis:{
                        events:{
                            afterSetExtremes: afterSetExtremes
                        },
                        minRange: 500
                    },
                    exporting:{
                        buttons:{
                            contextButton:{
                                symbol:"menu"
                            }
                        }
                    }
                },
                title : {
                    text : ""
                },
                series: [],
                loading: true,
                useHighStocks: true,
                func: function(chart) {
                    scope.chart = chart;
                }
            };

            function afterSetExtremes(e) {
                // if (scope.currentMode.text == scope.modes[1].text){
                //     if(e.trigger){
                //         var start = Math.round(e.min);
                //         var end = Math.round(e.max);
                //         dataService.getCiHistoryData(scope.baseurl,scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category, start, end);
                //     }
                //     console.log(e);
                //     console.log("start: ", new Date(e.min));
                //     console.log("end: ", new Date(e.max));
                //     console.log(scope.config.options.navigator.series);
                //     // todo load new data;
                // }

            }

            scope.delete = function () {
                scope.$emit(EVENT_DELETE_WIDGET,scope.dashboardindex,scope.widgetindex);
            };

            scope.openSettings = function () {
                var currentSettings = {};
                currentSettings.currentMode = scope.currentMode;
                currentSettings.title = scope.displayitem.title;
                currentSettings.modes = scope.modes;
                currentSettings.samplingRate = scope.samplingRate;
                dialogService.showWidgetSettings(currentSettings,function (newSettings) {
                    scope.currentMode = newSettings.newMode;
                    scope.displayitem.title = newSettings.newTitle;
                    scope.samplingRate = newSettings.newSamplingRate;
                });
            };

            //-------------------------- Listener -------------------------------------------------------------------------

            scope.$watch('currentMode',function(newMode, oldMode){
                if(oldMode != newMode){
                    clearData();
                    toggleLoading(true);
                    configureHowToLoadNewData(newMode,oldMode);
                    setChartTitle();
                    scope.$emit(EVENT_SAVE);
                }
            });

            scope.$watch('samplingRate',function (newSamplingRate, oldSamplingRate) {
                if (oldSamplingRate != newSamplingRate) {
                    updateSamplingRate(newSamplingRate);
                    scope.$emit(EVENT_SAVE);
                }
            });

            scope.$watch('displayitem.title',function (newTitle, oldTitle) {
                if (newTitle != oldTitle) {
                    setChartTitle();
                    scope.$emit(EVENT_SAVE);
                }
            });

            scope.$on(EVENT_ITEM_RESIZE,function(event,container){
                if (scope.chart && container == scope.chart.container){
                    scope.chart.reflow()
                }
            });

            scope.$on(EVENT_TOGGLE_EDIT_MODE,function(event, isEditing){
                scope.isEditing = isEditing;
                toggleVisibilityHighchartsButtons(isEditing);
            });

            scope.$on(EVENT_CI_LIVE_DATA_RECEIVED,function(event, status, baseUrl, ci, id, category, data){
                if (isforMe(baseUrl, ci, id, category) && scope.currentMode.text == scope.modes[0].text){
                    if(status){
                        if (!scope.config.series){
                            // create Series
                            scope.config.series = [{id:ci+id+category,data:[]}];
                            //little dirty hack für die editbuttons wenn ein neues diagramm hinzugefügt wird
                        }
                        toggleLoading(false);
                        if (scope.config.series[0].data.length < 60) {
                            scope.config.series[0].data.push([data.timestamp, data.value]);
                        } else {
                            scope.config.series[0].data.push([data.timestamp, data.value]);
                            scope.config.series[0].data.shift();
                        }
                    }else{
                        toastService.showErrorToast("Laden der Livedaten ist fehlgeschlagen");
                        scope.config.loading = 'ERROR'; // display Error in Highchart
                    }
                }else{
                    // data for other diagram, do nothing
                }
            });

            scope.$on(EVENT_CI_HISTORY_DATA_RECEIVED,function(event, status, baseUrl, ci, id, category, start, end, data){
                if (isforMe(baseUrl, ci, id, category) && scope.currentMode.text == scope.modes[1].text){
                    if(status){
                        if(start == scope.defaultHistorieStartValue && end == scope.defaultHistorieEndValue){
                            console.log("set navigator");
                            scope.config.options.navigator.series = data[0].data;
                            scope.config.options.navigator.adaptToUpdateData = false;
                            scope.config.options.scrollbar= { liveRedraw: false};
                        }
                        if(!scope.config.series){
                            scope.config.series = data;

                            toggleLoading(false);
                        }else{
                            clearData();
                            scope.config.series = data;
                        }
                    }else{
                        toastService.showErrorToast("Laden der Historiendaten ist fehlgeschlagen");
                        scope.config.loading = 'ERROR'; // display Error in Highchart
                    }
                }else{
                    // data for other diagram, do nothing
                }
            });

            scope.$on(EVENT_GATHERING_RATE_RECEIVED, function (event, status, baseUrl, ci, id, category, samplingRate) {
                if (isforMe(baseUrl, ci, id, category)){
                    if(status){
                        if(samplingRate > 500 && samplingRate < 10001){
                            scope.samplingRate = samplingRate;
                        }else{
                            scope.samplingRate = 1000;
                        }
                        if(scope.displayitem.realtime == true){
                            scope.currentMode = scope.modes[0]
                        }else{
                            scope.currentMode = scope.modes[1]
                        }

                    }else{
                        toastService.showErrorToast("Laden der Gathering Rate ist fehlgeschlagen");
                        scope.config.loading = 'ERROR'; // display Error in Highchart
                    }
                }else{
                    // data for other diagram, do nothing
                }
            });

            //-------------------------- Helper ----------------------------------------------------------------------------

            function isforMe(baseUrl, ci, id, category) {
                return baseUrl == scope.baseurl && ci == scope.displayitem.ci && id == scope.displayitem.id && category == scope.displayitem.category
            }

            function getSamplingRateForCi(baseUrl, ci, id, category) {
                dataService.getSamplingRateForCi(baseUrl, ci, id, category)
            }

            function toggleVisibilityHighchartsButtons(isEditing) {
                // hide or show all highcharts buttons
                var result = document.getElementsByClassName("highcharts-button");
                angular.forEach(result, function (object) {
                    if (isEditing) {
                        object.style.display = 'none'
                    } else {
                        object.style.display = 'block'
                    }
                });
            }

            function clearData() {
                //delete old data
                delete scope.config.series;
            }

            function toggleLoading(b) {
                scope.config.loading = b;
            }

            function toggleAnimation(b){
                scope.config.options.chart.animation = b;
            }

            function configureHowToLoadNewData(newMode, oldMode) {
                if (newMode.text == scope.modes[0].text){

                    toggleAnimation(false);
                    scope.displayitem.realtime = true;
                    dataService.enableCILiveTimer(scope.baseurl, scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category, scope.samplingRate);
                }
                if (newMode.text == scope.modes[1].text){


                    toggleAnimation(true);
                    scope.displayitem.realtime = false;
                    //define defaults
                    scope.defaultHistorieEndValue = new Date().getTime();
                    scope.defaultHistorieStartValue = scope.defaultHistorieEndValue-(1000*60*60*3); // start 3 hours ago
                    dataService.getCiHistoryData(scope.baseurl,scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category, scope.defaultHistorieStartValue, scope.defaultHistorieEndValue)
                }
                if (newMode.text == scope.modes[1].text && oldMode.text == scope.modes[0].text){

                    dataService.disableCiLiveTimer(scope.baseurl,scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category);
                }
            }

            function updateSamplingRate(newSamplingRate) {
                dataService.updateSamplingRateOfCiLiveTimer(scope.baseurl, scope.displayitem.ci, scope.displayitem.id, scope.displayitem.category, newSamplingRate)
            }

            function setChartTitle() {
                //wird immer als letztes bei einer Änderung aufgerufen, daher kann hiernach gespeichert werden
                delete scope.config.title.text;
                scope.config.title.text = scope.displayitem.title+ " - " +scope.currentMode.text;
            }

        }],
        link: function (scope, element) {

            element.on('$destroy', function() {
                dataService.disableCiLiveTimer(scope.baseurl,scope.displayitem.ci,scope.displayitem.id,scope.displayitem.category);
            });

        }
    };
}]);