'use strict';

/* Filters */

angular.module('appcatFilters', []).filter('checkmark', function() {
  return function(input) {
    return input ? '\u2713' : '\u2718';
  };

});
