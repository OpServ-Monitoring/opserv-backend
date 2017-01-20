/**
 * Created by Snare on 24.08.16.
 */
app.controller('DashboardCtrl',function($scope, $rootScope, prefService, $mdSidenav, toastService, dialogService, $filter, $translate){
    var scope = $scope;
    var rootScope = $rootScope;

    scope.isFabOpen = false;
    rootScope.isEditMode = false;

    scope.gridsterOpts = {
        columns: 30, // the width of the grid, in columns
        pushing: false, // whether to push other items out of the way on move or resize
        floating: false, // whether to automatically float items up so they stack (you can temporarily disable if you are adding unsorted items with ng-repeat)
        swapping: false, // whether or not to have items of the same size switch places instead of pushing down if they are the same size
        width: 'auto', // can be an integer or 'auto'. 'auto' scales gridster to be the full width of its containing element
        colWidth: 'auto', // can be an integer or 'auto'.  'auto' uses the pixel width of the element divided by 'columns'
        rowHeight: 'match', // can be an integer or 'match'.  Match uses the colWidth, giving you square widgets.
        margins: [15, 15], // the pixel distance between each widget
        outerMargin: true, // whether margins apply to outer edges of the grid
        isMobile: false, // stacks the grid items if true
        mobileBreakPoint: 500, // if the screen is not wider that this, remove the grid layout and stack the items
        mobileModeEnabled: true, // whether or not to toggle mobile mode when screen width is less than mobileBreakPoint
        minColumns: 1, // the minimum columns the grid must have
        minRows: 2, // the minimum height of the grid, in rows
        maxRows: 100,
        defaultSizeX: 2, // the default width of a gridster item, if not specifed
        defaultSizeY: 1, // the default height of a gridster item, if not specified
        //minSizeX: 20, // minimum column width of an item
        //maxSizeX: 40, // maximum column width of an item
        //minSizeY: 10, // minumum row height of an item
        //maxSizeY: 40 // maximum row height of an item
        resizable: {
            enabled: false,
            handles: ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw']
            //start: function(event, $element, widget) {}, // optional callback fired when resize is started,
            //resize: function(event, $element, widget) {}, // optional callback fired when item is resized,
            //stop: function(event, $element, widget) {} // optional callback fired when item is finished resizing
        },
        draggable: {
            enabled: false, // whether dragging items is supported
            //handle: '.my-class' // optional selector for drag handle
            //start: function(event, $element, widget) {}, // optional callback fired when drag is started,
            //drag: function(event, $element, widget) {}, // optional callback fired when item is moved,
            stop: function(event, $element, widget) { save(); } // optional callback fired when item is finished dragging
        }
    };

    prefService.getDashboards();

    scope.$on(EVENT_DASHBOARDS_RECEIVED,function(event,success,dashboards){
        if (success){
            rootScope.dashboards=dashboards;
        }else{
            toastService.showErrorToast("Laden der Dashboards fehlgeschlagen!")
        }
        scope.isLoaded = true;
    });

    scope.$on(EVENT_DELETE_WIDGET, function (event, dashboardIndex, widgetIndex) {
        var forRollback = rootScope.dashboards[dashboardIndex].widgets[widgetIndex];
        rootScope.dashboards[dashboardIndex].widgets.splice(widgetIndex,1);
        toastService.showDeletedToast("Widget",function (response) {
            if ( response == 'ok' ) {
                rootScope.dashboards[dashboardIndex].widgets.push(forRollback);
                save();
            }
        });
        save();
    });

    scope.$on(EVENT_SAVE, function (event) {
        save();
    });

    scope.openSettingsOpservDialog = function () {
        dialogService.showOpservSettings(function (newSettings) {

        });
    };

    scope.openLanguageDialog = function () {
        dialogService.showLanguageDialog($rootScope.selectedLanguageKey,function (newLanguageKey) {
            $rootScope.selectedLanguageKey = newLanguageKey;
            $translate.use(newLanguageKey);
            localStorage.setItem('language',newLanguageKey);
        });
    };

    scope.addDashboard = function(){
        rootScope.dashboards.push({
            title: 'My Dashboard',
            widgets:[],
            baseUrl: ''
        });
        save();
    };

    scope.deleteCurrentDashboard = function(index){
        var forRollback = rootScope.dashboards[index];
        rootScope.dashboards.splice(index,1);
        toastService.showDeletedToast("Dashboard",function (response) {
            if ( response == 'ok' ) {
                rootScope.dashboards.push(forRollback);
                save();
            }
        });
        save();
    };

    scope.addWidget = function(ci, id, cat){
        var widget = {
            sizeX: 15,
            sizeY: 10,
            row: 0,
            col: 0,
            displayItem: {
                ci: ci.label,
                category: cat.label,
                realtime: true,
                samplingRate: 1000,
                displayAsChart:true
            }
        };

        if (id != undefined){
            widget.displayItem.id=id.label;
            widget.displayItem.title=ci.label+" "+id.label+" "+cat.label
        }else{
            widget.displayItem.id=undefined;
            widget.displayItem.title=ci.label+" "+cat.label
        }

        rootScope.dashboards[scope.selectedDashboard].widgets.push(widget);
        save();
    };

    scope.toggleEditMode = function(){

        if(!scope.isEditMode){
            scope.gridsterOpts.pushing = true;
            scope.gridsterOpts.floating = true;
            scope.gridsterOpts.swapping = true;
            scope.gridsterOpts.resizable.enabled = true;
            scope.gridsterOpts.draggable.enabled = true;
            rootScope.$broadcast(EVENT_TOGGLE_EDIT_MODE,true);
        }else{
            scope.gridsterOpts.pushing = false;
            scope.gridsterOpts.floating = false;
            scope.gridsterOpts.swapping = false;
            scope.gridsterOpts.resizable.enabled = false;
            scope.gridsterOpts.draggable.enabled = false;
            rootScope.$broadcast(EVENT_TOGGLE_EDIT_MODE,false);
        }
        rootScope.isEditMode = !rootScope.isEditMode;
        $mdSidenav('left').toggle();
        save();
    };

    scope.toggleLeft = function () {
        $mdSidenav('left').toggle();
    };

    function save() {
        prefService.saveDashboards(scope.dashboards);
    }

});
