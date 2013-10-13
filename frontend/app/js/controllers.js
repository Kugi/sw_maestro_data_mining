'use strict';

/* Controllers */
function AppListCtrl($scope, $http, $resource, App, Test) {
	$scope.orderProp = 'score';
    $http.defaults.useXDomain = true;
    //$scope.apps = App.get_list();

	$scope.autocom = function() {
		$scope.apps = App.auto_comp({name: $scope.query});

	};







//    $scope.title = "zzzzzzzzDemoCtrl";
//    $scope.d3Data = [
//        {name: "Greg", score:98},
//        {name: "Ari", score:96},
//        {name: "Loser", score: 48}
//    ];
//    $scope.d3OnClick = function(item){
//        alert(item.name);
//    };
}



//id: $routeParams.appId
function AppDetailCtrl($scope, $routeParams, App, Test, Test2, Test3) {
	$scope.appiidd = $routeParams.appId;

    $scope.app = App.get({id: $routeParams.appId}, function(app) {
        $scope.mainImageUrl = app.img;
    });

    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    };

	$scope.hello = function(name) {
		alert('Hello ' + (name || 'world') + '!');
	};

    $scope.test = Test.add({a:21, b:13});


    $scope.test2 = Test2.genderboy({appId:$scope.appiidd}, function(data2){
        $scope.test = 'xxxx';
        Test3.gendergirl({appId:$scope.appiidd}, function(data3){
            $scope.results = resultsA;
            var resultsA = {
                Sex: {
                    _type: "terms",
                    terms: [{
                        term: "Male",
                        count: data2.num
//                count: $scope.test2num
                    }, {
                        term: "Female",
//                count: $scope.test3num
                        count: data3.num
                    }]
                }
            };
            $scope.results = resultsA;
//            $scope.test3num = data3;
//            $scope.results = resultsA;
        });


//        $scope.test2num = data2;
//        Test3.gendergirl({appId:$scope.appiidd} ,function(data3){
//            $scope.test3num = data3;
//            $scope.results = resultsA;
//        });
    });

////
//    $scope.test3 = Test3.gendergirl({appId:$scope.appiidd});
//
//
//    $scope.results = resultsA;
//    var resultsA = {
//        Sex: {
//            _type: "terms",
//            terms: [{
//                term: "Male",
//                count: 50
////                count: $scope.test2num
//            }, {
//                term: "Female",
////                count: $scope.test3num
//                count: 80
//            }]
//        }
//    };
}
AppDetailCtrl.$inject = ['$scope', '$routeParams', 'App', 'Test', 'Test2', 'Test3'];



function DemoCtrl($scope) {
    $scope.title = "DemoCtrl";
    $scope.d3Data = [
        {name: "Greg", score:98},
        {name: "Ari", score:96},
        {name: "Loser", score: 48}
    ];
    $scope.d3OnClick = function(item){
        alert(item.name);
    };
}


function DemoCtrl2($scope) {
    $scope.title = "DemoCtrl2";
    $scope.d3Data = [
        {title: "Greg", score:12},
        {title: "Ari", score:43},
        {title: "Loser", score: 87}
    ];
}


/*
//id: $routeParams.appId
function AppDetailCtrl($scope, $routeParams, App2) {
	$scope.appiidd = $routeParams.appId;
    $scope.app = App2.get({id: $routeParams.appId}, function(app) {
        $scope.mainImageUrl = app.img;
    });

    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    }
	$scope.hello = function(name) {
		alert('Hello ' + (name || 'world') + '!');
	}
}
AppDetailCtrl.$inject = ['$scope', '$routeParams', 'App'];




*/

/*
function PhoneListCtrl($scope) {
	$scope.phones = [
		{"name": "Nexus S",
		 "snippet": "Fast just got faster with Nexus S."},
		{"name": "Motorola XOOM™ with Wi-Fi",
		 "snippet": "The Next, Next Generation tablet."},
		{"name": "MOTOROLA XOOM™",
		 "snippet": "The Next, Next Generation tablet."}
	];
	$scope.hello = "Hello, World!"
}
*/
