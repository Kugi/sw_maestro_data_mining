'use strict';

/* App Module */

angular.module('appcat', [
        'appcatFilters',
        'appcatServices',
        'graph.directives',
        'dangle',
        'appcat.controllers']).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/apps', {templateUrl: 'app/partials/app-list.html',   controller: AppListCtrl}).
      when('/apps/:appId', {templateUrl: 'app/partials/app-detail.html', controller: AppDetailCtrl}).
      when('/apps/:appId/detail', {templateUrl: 'app/partials/detail.html', controller: DetailCtrl}).
      when('/apps/:appId/detail2', {templateUrl: 'app/partials/detail2.html', controller: DetailCtrl2}).
      otherwise({redirectTo: '/apps'});
}]).config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common["X-Requested-With"];
        $httpProvider.defaults.headers.common["Accept"] = "application/json, text/plain, * / *";
        $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
    }]);

angular.module('d3', []);
angular.module('graph.directives', ['d3']); //module direcitves의 graph.~~모듈에 d3가 종속되있다.
//angular.module('myApp.directives'. ['d3']);
angular.module('appcat.controllers', [])
    .controller('DemoCtrl', function($scope) {
        'use strict';
    });

angular.module('myApp', [])
    .controller('myCtrl', function ($scope) {
    })
    .directive('hboTabs', function() {
        return {
            restrict: 'A',
            link: function(scope, elm, attrs) {
                var jqueryElm = $(elm[0]);
                $(jqueryElm).tabs()
            }
        };
    });


