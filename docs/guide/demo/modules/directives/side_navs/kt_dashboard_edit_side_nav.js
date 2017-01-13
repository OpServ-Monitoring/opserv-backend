/**
 * Created by Snare on 07.09.16.
 */
app.directive('ktDashboardEditSideNav',[ 'dataService','toastService', 'dialogService',  function(dataService,toastService, dialogService){
    return {
        priority: 1,

        templateUrl: 'views/templates/side_navs/kt_dashboard_edit_side_nav.html',

        restrict: 'E',
        controller: ['$scope','$rootScope','$timeout', function MyTabsController($scope,$rootScope,$timeout) {

            const CI_MEMORY = "memory";
            const CI_SYSTEM = "system";

            const OPTION_DASHBOARD_SETTINGS = "edit dashboard Settings";
            const OPTION_ADD_WIDGET = "add widget";

            var scope = $scope;
            var rootScope = $rootScope;

            scope.lastTabs = [];

            scope.generalOptions=[
                {label:OPTION_DASHBOARD_SETTINGS,action:selectOption},
                {label:OPTION_ADD_WIDGET,action:selectOption}
            ];

            scope.cis =[];

            scope.ids = [];

            scope.categories = [];

            function loadCis() {
                dataService.getCIs(rootScope.dashboards[scope.selectedDashboard].baseUrl);
            }

            function loadIds(ci) {
                dataService.getCiIds(ci.label,rootScope.dashboards[scope.selectedDashboard].baseUrl);
            }

            function loadCats(id) {
                dataService.getCiCats(scope.selectedCi.label,id,rootScope.dashboards[scope.selectedDashboard].baseUrl);
            }

            function loadMemoryCats() {
                dataService.getMemoryCats(scope.selectedCi.label,rootScope.dashboards[scope.selectedDashboard].baseUrl);
            }

            scope.$on(EVENT_CIS_RECEIVED, function (event, status, cis) {
                if(status){
                    scope.cis = [];
                    angular.forEach(cis,function(ci){
                        switch (ci) {
                            case CI_MEMORY:
                                scope.cis.push({label:ci,action:selectMemoryCi});
                                break;
                            case CI_SYSTEM:
                                // exclude System access from user
                                break;
                            default:
                                scope.cis.push({label:ci,action:selectCi})
                        }
                    });
                    if(scope.cis.length==0){
                        scope.cis.push({label:"not supported",action:{}})
                    }
                    scope.cisLoading = false;
                }else{
                    toastService.showErrorToast("Laden der Ci's fehlgeschlagen");
                }
            });

            scope.$on(EVENT_CI_IDS_RECEIVED, function (event, status, ciName, ids) {
                if(status){
                    if(ciName==scope.selectedCi.label){
                        scope.ids = [];
                        angular.forEach(ids,function(id){
                            scope.ids.push({label:id,action:selectId})
                        });
                        if(scope.ids.length==0){
                            scope.ids.push({label:"not supported",action:{}})
                        }else{
                            loadCats(scope.ids[0].label);
                        }
                        scope.idsLoading = false;
                    }
                }else{
                    toastService.showErrorToast("Laden der Id's fehlgeschlagen");
                }
            });

            scope.$on(EVENT_CI_CATS_RECEIVED, function (event, status, ciName, cats) {
                if(status){
                    if(ciName==scope.selectedCi.label){
                        scope.categories = [];
                        angular.forEach(cats,function(catName){
                            scope.categories.push({label:catName,action:selectCategory})
                        });
                        scope.catsLoading = false;
                    }
                }else{
                    toastService.showErrorToast("Laden der Kategorien fehlgeschlagen");
                }
            });

            scope.$on(EVENT_MEMORY_CATS_RECEIVED, function (event, status, ciName, cats) {
                if(status){
                    if(ciName==scope.selectedCi.label){
                        scope.categories = [];
                        angular.forEach(cats,function(catName){
                            scope.categories.push({label:catName,action:selectCategory})
                        });
                        scope.catsLoading = false;
                    }
                }else{
                    toastService.showErrorToast("Laden der Kategorien fehlgeschlagen");
                }
            });

            function selectOption(option) {
                if (option.label == OPTION_ADD_WIDGET){
                    scope.selectedSideNavIndex = 1;//Ci Auswahl
                    scope.lastTabs.push(0);
                    scope.cisLoading= true;
                    loadCis();
                }
                if (option.label == OPTION_DASHBOARD_SETTINGS){
                    var currentSettings = {};
                    currentSettings.baseUrl = rootScope.dashboards[scope.selectedDashboard].baseUrl;
                    currentSettings.title = rootScope.dashboards[scope.selectedDashboard].title;
                    dialogService.showDashboardSettings(currentSettings,function (newSettings) {
                        console.log("neue Settings", newSettings);
                        dataService.updateAllBaseUrlRelatedIntervals(rootScope.dashboards[scope.selectedDashboard].baseUrl,newSettings.newBaseUrl,rootScope.dashboards[scope.selectedDashboard].widgets);
                        rootScope.dashboards[scope.selectedDashboard].title = newSettings.newTitle;
                        rootScope.dashboards[scope.selectedDashboard].baseUrl = newSettings.newBaseUrl;
                        scope.$emit(EVENT_SAVE);
                    })
                }
            }

            function selectCi (ci) {
                scope.selectedSideNavIndex = 2;//ID Auswahl
                scope.lastTabs.push(1);
                scope.idsLoading= true;
                loadIds(ci);
                scope.catsLoading= true;
                scope.selectedCi = ci;
            }

            function selectId (id) {
                scope.selectedSideNavIndex = 3;//Kategorie Auswahl
                scope.lastTabs.push(2);
                scope.selectedId = id;
            }

            function selectCategory(cat){
                scope.selectedCat = cat;
                scope.addWidget(scope.selectedCi,scope.selectedId,scope.selectedCat);
            }

            function selectMemoryCi(ci){
                scope.selectedSideNavIndex = 3;//Kategorie Auswahl
                scope.lastTabs.push(1);
                scope.catsLoading = true;
                scope.selectedCi = ci;
                scope.selectedId = undefined;
                loadMemoryCats();
            }

            scope.scrollBack = function () {
                scope.selectedSideNavIndex = scope.lastTabs.pop();
            };

            scope.$watch('selectedSideNavIndex',function(newValue,oldValue){
                if(scope.selectedSideNavIndex == 0 || scope.selectedSideNavIndex == 1){
                    scope.ids=[];
                    scope.categories=[];
                }
                if(scope.selectedSideNavIndex == 0){
                    scope.cis=[];
                }
            });

            scope.$on(EVENT_TOGGLE_EDIT_MODE,function(event, isEditing){
                scope.selectedSideNavIndex = 0;
                scope.lastTabs=[];
            });
        }]
    };
}]);