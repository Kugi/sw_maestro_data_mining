'use strict';

/* Services */

angular.module('appcatServices', ['ngResource']).
    factory('App', function($resource){
        return $resource('http://17.buzzni.com/app', {}, {
            get_list: {method:'GET', params:{'func':'get_list'},isArray:true},
            get: {method:'GET', params:{'func': 'get_info'}, isArray:false},
            auto_comp: {method:'GET', params:{'func': 'autocomplete'}, isArray:true}

  })}).
    factory('Min', function($resource){
        return $resource('http://soma3.buzzni.com:port/app', {port:":83"}, {
            add: {method:'GET', params:{'func':'add'}, isArray:false},
            get_count_gender: {method: 'GET', params:{'func' : 'get_count_gender'}, isArray:false},
            get_count_age: {method: 'GET', params:{'func' : 'get_count_age'}, isArray:false},

            weekDay: {method: 'GET', params:{'func' : 'weekDay'}, isArray:false},
            addWeekday: {method: 'GET', params:{'func' : 'addWeekday'}, isArray:false},
            date_app: {method: 'GET', params:{'func' : 'date_app'}, isArray:false},
            process: {method: 'GET', params:{'func' : 'process'}, isArray:true},
            process2: {method: 'GET', params:{'func' : 'process2'}, isArray:false},
            process3: {method: 'GET', params:{'func' : 'process3'}, isArray:false},
            wow_cluster: {method: 'GET', params:{'func' : 'wow_cluster'}, isArray:true}
        })});


