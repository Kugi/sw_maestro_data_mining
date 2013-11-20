
/* Controllers */
function AppListCtrl($scope,$http,$resource, App, Min) {
    $scope.orderProp = 'age';
    $http.defaults.useXDomain = true;
    $scope.apps = App.get();


    $scope.autocom = function(){
        $scope.apps = App.auto_comp({name: $scope.query});
//        var a = App.auto_comp({name: $scope.query});
//        var a = {
//            "alias": "Kakao Corp.",
//            "code": "com.kakao.style",
//            "name": "카카오스타일-KakaoStyle-패션,쇼핑,스타일!",
//            "img": "https://lh3.ggpht.com/beMnDa8Kb3NavMvnpbXNTKCFmkBWeR9z3BWhcbWkJYAiGsNW4pkRraJ3YM0b8xadDg=w300",
//            "install_total": "18497",
//            "usage_total": "3067",
//            "id": "1860060",
//            "cate": "app"
//        }
        var array = [1,2,3,4]
//        //For test autocom, if it is changed, screen updates...
//        for (var i in array){
//            $scope.test1 += i;
//        }
    }

    $scope.test = Min.add({a:2, b:3});
//  Min.get_count_gender({app : 1525767}, function(d){
//        $scope.ggg = d;
//    });
}
AppListCtrl.$inject = ['$scope','$http','$resource','App', 'Min'];


function AppDetailCtrl($scope, $routeParams, App, Min) {
    Min.get_count_gender({app : $routeParams.appId}, function(d){
        var rate = d.male/(d.male+ d.female) * 100
        $scope.bar1 = [{"name":"남성("+Math.floor(rate)+"%)", "score": rate},
                       {"name":"여성("+Math.floor(100-rate)+"%)", "score": (100 - rate)}];

    });



    $scope.app = App.get({id: $routeParams.appId}, function(app) {

        $scope.mainImageUrl = app.img;
        $scope.id = $routeParams.appId;
        $scope.cluster = Min.wow_cluster({id : $routeParams.appId}, function(cluster){
            var name_ = app.name;
//            $scope.app_ = App.auto_comp({name: name_});
//            var id0 = app_.id;
//            id0 = Number(id0);
//            console.log(cluster[0]);
            $scope.whatthe = cluster


            var list = cluster;
            list = list.sort( function(a, b) {
               return a.value - b.value;
            });

            $scope.ctest = list;
            $scope.others0 = App.get({id: cluster[1].id});
            $scope.others1 = App.get({id: cluster[2].id});
            $scope.others2 = App.get({id: cluster[3].id});
            $scope.others3 = App.get({id: cluster[4].id});
            $scope.others4 = App.get({id: cluster[5].id});

        });

        $scope.ages = Min.get_count_age({app : $routeParams.appId}, function(ages){
            $scope.testage = ages
            var tot = ages.one + ages.two + ages.three + ages.four
            var one = ages.one
            var two = ages.two
            var three = ages.three
            var four = ages.four

            var resultsA = {
                Sex: {
                    _type: "terms",
                    terms: [{
                        term: "10대",
                        count: one
                    }, {
                        term: "20대",
                        count: two
                    }, {
                        term: "30대",
                        count: three
                    }, {
                        term: "40대",
                        count: four
                    }]
                }
            };
            $scope.results = resultsA;
        });
    });

    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    };
    $scope.d3OnClick = function(item){
        alert(item.name);
    };


}
//AppDetailCtrl.$inject = ['$scope','$http','$resource','App', 'Min'];


function DetailCtrl($scope, $routeParams, App, Min) {
//    Min.date_app({id_ : $routeParams.appId}, function(cnt_weekday){
//        $scope.weekday = cnt_weekday;
//    });

    Min.process({id_: $routeParams.appId}, function(proce){
        $scope.pro = proce
    });

    Min.process2({id_: $routeParams.appId}, function(dataa){
        $scope.pro2 = dataa
    });

    Min.process3({id_: $routeParams.appId}, function(dataa){
        $scope.pro3 = dataa
    });

    $scope.id = $routeParams.appId
    var age10 = 300
    var age20 = 100
    var age30 = 200
    var resultsA = {
        Sex: {
            _type: "terms",
            terms: [{
                term: "10대",
                count: age10
            }, {
                term: "20대",
                count: age20
            }, {
                term: "30",
                count: age30
            }]
        }
    };
    $scope.resultsa = resultsA;

    var temp = 50;
    var date = 1341100800000+3600000*12; // jul 08
    Min.date_app({id_:$routeParams.appId}, function(weekday){
        $scope.weekday = weekday
        var resultsB = {
            facets: {
                Times: {
                    _type: "date_histogram",
                    entries: [
                        {
                            time: 86400000*3,
                            count: weekday.mon
                        },
                        {
                            time: 86400000*4,
                            count: weekday.tue
                        },
                        {
                            time: 86400000*5,
                            count: weekday.wed
                        },
                        {
                            time: 86400000*6,
                            count: weekday.thu
                        },
                        {
                            time: 86400000*7,
                            count: weekday.fri
                        },
                        {
                            time: 86400000*8,
                            count: weekday.sat
                        },
                        {
                            time: 86400000*9,
                            count: weekday.sun
                        }
                    ]
                }
            }
        };
        var resultsB_ = {
            facets: {
                Times: {
                    _type: "date_histogram",
                    entries: [
                        {
                            time: 86400000*2,
                            count: weekday.sun
                        },
                        {
                            time: 86400000*3,
                            count: weekday.mon
                        },
                        {
                            time: 86400000*4,
                            count: weekday.tue
                        },
                        {
                            time: 86400000*5,
                            count: weekday.wed
                        },
                        {
                            time: 86400000*6,
                            count: weekday.thu
                        },
                        {
                            time: 86400000*7,
                            count: weekday.fri
                        },
                        {
                            time: 86400000*8,
                            count: weekday.sat
                        }
                    ]
                }
            }
        };

        $scope.filterSearchB = function (type, term) {
            switch (currentResults) {
                case 'A':
                    $scope.results_histo = resultsB_;
                    currentResults = 'B';
                    break;
                case 'B':
                    $scope.results_histo = resultsB;
                    currentResults = 'A';
                    break;
            }
        };
        $scope.results_histo = resultsB;
        var currentResults = 'A';

    });
    var ii = 2
    Min.process({id_: $routeParams.appId, ic: ii+1}, function(data1){
        var oneday = 2678400000/30.4;
        var resultsC = {
            facets: {
                Times: {
                    _type: "date_histogram",
                    entries: [
                        {

                            time: date,
                            count: data1[0].count
                        },
                        {
                            time: date+oneday,
                            count: data1[1].count
                        },
                        {
                            time: date+oneday*2,
                            count: data1[2].count
                        },
                        {
                            time: date+oneday*3,
                            count: data1[3].count
                        },
                        {
                            time: date+oneday*4,
                            count: data1[4].count
                        },
                        {
                            time: date+oneday*5,
                            count: data1[5].count
                        },
                        {
                            time: date+oneday*6,
                            count: data1[6].count
                        }
                    ]
                }
            }
        };

        $scope.resultss = resultsC;
    });
    var resultsC_ = {
//        facets: {
//            Times: {
//                _type: "date_histogram",
//                entries: [
//                    {
//                        time: 1343779200000,
//                        count: temp
//                    }
//                    ,
//                    {
//                        time: 1346457600000,
//                        count: 78
//                    },
//                    {
//                        time: 1349049600000,
//                        count: 45
//                    },
//                    {
//                        time: 1351728000000,
//                        count: 134
//                    }
//                ]
//            }
//        }
    };

    $scope.filterByDate = function (type, term) {
        switch (currentResults) {
            case 'A':
                $scope.results = resultsC;
                currentResults = 'B';
                break;
            case 'B':
                $scope.results = resultsC_;
                currentResults = 'A';
                break;
        }
    };
    var onemonth = 2678400000
    Min.process2({id_: $routeParams.appId}, function(data1){
        var resultsD = {
            facets: {
                Times: {
                    _type: "date_histogram",
                    entries: [
                        {
                            time: 1343779200000+5.8*onemonth,
                            count: data1.m2
                        },
                        {
                            time: 1346457600000+6*onemonth,
                            count: data1.m3
                        },
                        {
                            time: 1349049600000+6.3*onemonth,
                            count: data1.m4
                        },
                        {
                            time: 1351730000000+6.6*onemonth,
                            count: data1.m5
                        },
                        {
                            time: 1353760000000+6.7*onemonth,
                            count: data1.m6
                        },
                        {
                            time: 1356728000000+6.8*onemonth,
                            count: data1.m7
                        }
                    ]
                }
            }
        };
        $scope.resultsss = resultsD;
    });
    Min.process3({id_: $routeParams.appId}, function(data1){
        var resultsE = {
            facets: {
                Times: {
                    _type: "date_histogram",
                    entries: [
                        {
                            time: 1343779200000+5.8*onemonth,
                            count: data1.w0
                        },
                        {
                            time: 1346457600000+6*onemonth,
                            count: data1.w1
                        },
                        {
                            time: 1349049600000+6.3*onemonth,
                            count: data1.w2
                        },
                        {
                            time: 1351730000000+6.6*onemonth,
                            count: data1.w3
                        },
                        {
                            time: 1353760000000+6.7*onemonth,
                            count: data1.w4
                        },
                        {
                            time: 1356728000000+6.8*onemonth,
                            count: data1.w5
                        },
                        {
                            time: 1356728000000+7*onemonth,
                            count: data1.w6
                        }
                    ]
                }
            }
        };
        $scope.resultdown = resultsE;
    });
    var currentResults = 'A';
}


function DetailCtrl2($scope, $routeParams, App, Min) {


}
