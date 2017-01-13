app.factory('toastService',function($mdToast){

    var service = {};

    service.showDeletedToast = function (whatWasDeleted, callback) {
        var toast = $mdToast.simple()
            .textContent(whatWasDeleted+' gelöscht ')
            .action('UNDO')
            .highlightAction(true)
            .highlightClass('md-accent')// Accent is used by default, this just demonstrates the usage.
            .position("top left")
            .hideDelay(5000);

        $mdToast.show(toast).then(function(response) {
            callback(response)
        });
    };

    service.showErrorToast = function (errorText) {
        $mdToast.show({
            hideDelay   :   3000,
            position    :   'top left',
            template    :   '<md-toast> ' +
                            '<div flex style="color:#FF5722" >Error</div> ' +
                            '<div >'+errorText+'</div> ' +
                            '</md-toast>'
        });
    };

    return service;
});

