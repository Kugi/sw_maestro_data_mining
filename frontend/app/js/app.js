'use strict';

/* App Module */
(function () {
    angular.module('appcat', [
            'appcatFilters',
            'appcatServices',
            'appcatDirectives',
            'dangle'
        ]).
        config(['$routeProvider', function($routeProvider) {
        $routeProvider.
            when('/apps', {templateUrl: 'app/partials/app-list.html', controller: AppListCtrl}).
            when('/apps/:appId', {templateUrl: 'app/partials/app-detail.html', controller: AppDetailCtrl}).
            otherwise({redirectTo: '/apps'});
    }]).config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common["X-Requested-With"];
        $httpProvider.defaults.headers.common["Accept"] = "application/json, text/plain, * / *";
        $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
    }]);

//    angular.module('app', ['dangle', 'demo.controllers']);
    angular.module('d3', ['dangle']);
    angular.module('appcatDirectives', ['d3']);


}());