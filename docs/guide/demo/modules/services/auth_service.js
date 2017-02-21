
app.factory('authService',function($rootScope){

//------------------------------------------------ Variablen -------------------------------------------------------------------------------------------------------------------------------------//
    var service = {};

//------------------------------------------------ Funktionen --------------------------------------------------------------------------------------------------------------------------------------//
    var isLoggedIn = false;

    service.isLoggedIn = function () {
        if ($rootScope.isMock){
            return true; // Always return true on mock usage
        }
        return  isLoggedIn;
    };

    service.setLogin = function (bool) {
        isLoggedIn = bool;
    };

    return service;
});

