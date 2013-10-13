'use strict';

/* Services */

angular.module('appcatServices', ['ngResource']).
    factory('App', function($resource){
        return $resource('http://17.buzzni.com/app', {}, {
            //get_list: {method:'GET', params:{func:'get_list'}, isArray:true},
			get: {method:'GET', params:{func:'get_info'}, isArray:false},
			auto_comp: {method:'GET', params:{func:'autocomplete', num:'20'}, isArray:true}
	    })

}).factory('Test', function($resource){
        return $resource('http://soma3.buzzni.com:port/app', {port:':82'}, {
            add: {method:'GET', params:{func:'add'}, isArray:false}
        })

}).factory('Test2', function($resource){
        return $resource('http://soma3.buzzni.com:port/app', {port:':82'}, {
            genderboy: {method:'GET', params:{func:'genderboy'}, isArray:false}
        })

}).factory('Test3', function($resource){
        return $resource('http://soma3.buzzni.com:port/app', {port:':82'}, {
            gendergirl: {method:'GET', params:{func:'gendergirl'}, isArray:false}
        })
})
;

