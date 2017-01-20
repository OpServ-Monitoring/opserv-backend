/**
 * Created by Snare on 24.08.16.
 */
app.controller('LoginCtrl',function($location, authService, dialogService){

    if (!authService.isLoggedIn()){
        dialogService.showLoginDialog(function (status) {
            if(status){
                $location.path('/');
            }
        })
    }else{
        $location.path('/');
    }
});
