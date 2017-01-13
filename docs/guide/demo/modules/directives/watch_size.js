/**
 * Created by Snare on 28.08.16.
 */
/*
 * Checks every $digest for height changes
 */
app.directive( 'ktWatchSize', ['$rootScope',function(rootScope) {
    return {
        link: function( scope, element, attrs ) {
            var container;
            scope.$watch( function() {
                if(scope.__height != element[0].offsetHeight ){
                    if(element[0].children[0]
                        && element[0].children[0].children[0]
                        && element[0].children[0].children[0].children[0])
                    {
                        container = element[0].children[0].children[0].children[0];
                        rootScope.$broadcast(EVENT_ITEM_RESIZE,container,element);
                        scope.__height = element[0].offsetHeight;
                    }
                }
                if(scope.__width != element[0].offsetWidth){
                    if(element[0].children[0]
                        && element[0].children[0].children[0]
                        && element[0].children[0].children[0].children[0])
                    {
                        container = element[0].children[0].children[0].children[0];
                        rootScope.$broadcast(EVENT_ITEM_RESIZE,container,element);
                        scope.__width = element[0].offsetWidth;
                    }

                }


                //if(scope.__height != element[0].offsetHeight ){
                //    if(element[0].children[0]
                //        && element[0].children[0].children[0]
                //        && element[0].children[0].children[0].children[0]
                //        && element[0].children[0].children[0].children[0].children[0])
                //    {
                //        container = element[0].children[0].children[0].children[0].children[0];
                //        rootScope.$broadcast('item-resize',container,element);
                //        scope.__height = element[0].offsetHeight;
                //    }
                //}
                //if(scope.__width != element[0].offsetWidth){
                //    if(element[0].children[0]
                //        && element[0].children[0].children[0]
                //        && element[0].children[0].children[0].children[0]
                //        && element[0].children[0].children[0].children[0].children[0])
                //    {
                //        container = element[0].children[0].children[0].children[0].children[0];
                //        rootScope.$broadcast('item-resize',container,element);
                //        scope.__width = element[0].offsetWidth;
                //    }
                //
                //}
            });
        }
    }
}]);