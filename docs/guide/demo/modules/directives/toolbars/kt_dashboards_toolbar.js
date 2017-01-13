/**
 * Created by Snare on 07.09.16.
 */
app.directive('ktDashboardsToolbar', function(){
    return {
        priority: 1,

        templateUrl: 'views/templates/toolbars/kt_dashboards_toolbar.html',

        restrict: 'E'
    };
});