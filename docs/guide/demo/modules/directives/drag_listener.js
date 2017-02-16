/**
 * Created by Snare on 28.08.16.
 */
/*
 * Checks every $digest for height changes
 */
app.directive( 'dragListener', ['$rootScope',function(rootScope) {
    return {
        link: function( scope, element, attrs ) {
            console.log("test");
            element.on('$md.pressup', function() {
                rootScope.$broadcast(EVENT_SLIDER_DRAG_END, element[0].attributes[5].nodeValue,element[0].id);
            });
        }
    }
}]);
