app.factory('toastService',function($mdToast){

    var service = {};

    service.showRollbackToast = function (whatWasDeleted, callback) {
        var toast = $mdToast.simple()
            .textContent(whatWasDeleted+' gelöscht ')
            .action('UNDO')
            .highlightAction(true)
            .highlightClass('md-accent')// Accent is used by default, this just demonstrates the usage.
            .position("bottom left")
            .hideDelay(5000);

        $mdToast.show(toast).then(function(response) {
            if ( response == 'ok' ) {
                callback(true)
            }else{
                callback(false)
            }

        });
    };

    service.showErrorToast = function (errorText) {
        $mdToast.show({
            hideDelay   :   3000,
            position    :   'bottom left',
            template    :   '<md-toast>' +
                            '<div flex="20" style="color:#FF5722" >Error</div>' +
                            '<div flex="80">'+errorText+'</div>' +
                            '</md-toast>'
        });
    };

    return service;
});

