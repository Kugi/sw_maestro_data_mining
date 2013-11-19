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
//            weekDay: {method: 'GET', params:{'func' : 'weekDay'}, isArray:false},
//            addWeekday: {method: 'GET', params:{'func' : 'addWeekday'}, isArray:false},
//            date_app: {method: 'GET', params:{'func' : 'date_app'}, isArray:false},
            process: {method: 'GET', params:{'func' : 'process'}, isArray:true},

            process2: {method: 'GET', params:{'func' : 'process2'}, isArray:false},

//            process3: {method: 'GET', params:{'func' : 'process3'}, isArray:false},

            weekDay_new: {method: 'GET', params:{'func' : 'weekDay_new'}, isArray:true},
            date_new: {method: 'GET', params:{'func': 'date_new'}, isArray:true},
            date_new2: {method: 'GET', params:{'func': 'date_new2'}, isArray:true}

//            get_cluster_test: {method:'GET', params:{'func': 'get_cluster_test'}, isArray:false}

        })});



