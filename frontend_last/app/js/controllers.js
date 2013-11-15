
/* Controllers */
function AppListCtrl($scope,$http,$resource, App, Min) {
  $scope.orderProp = 'age';
    $http.defaults.useXDomain = true;
    $scope.apps = App.get_list({name: $scope.query});

  $scope.autocom = function(){
    $scope.apps_with_thumb = App.get_list({name: $scope.query});
    $scope.apps = App.auto_comp({name: $scope.query});

  }

  $scope.test = Min.add({a:5, b:3});
//  Min.get_count_gender({app : 1525767}, function(d){
//        $scope.ggg = d;
//    });

}



function DetailCtrl2($scope, $routeParams, App, Min) {
//    alert("zzzDc2");

    var currentCodeFlower;
    var createCodeFlower = function(json) {
        // update the jsonData textarea
        document.getElementById('jsonData').value = JSON.stringify(json);
        // remove previous flower to save memory
        if (currentCodeFlower) currentCodeFlower.cleanup();
        // adapt layout size to the total number of elements
        var total = countElements(json);
        w = parseInt(Math.sqrt(total) * 30, 10);
        h = parseInt(Math.sqrt(total) * 30, 10);
        // create a new CodeFlower
        currentCodeFlower = new CodeFlower("#cluster_visual1_1", w, h).update(json);
    };

    d3.json('app/data/testData.json', createCodeFlower);

//                    document.getElementById('project').addEventListener('change', function() {
//                        d3.json(this.value, createCodeFlower);
//                    });
    document.getElementById('jsonInput').addEventListener('submit', function(e) {
        e.preventDefault();
        document.getElementById('cluster_visual1_1').scrollIntoView();
        var json = JSON.parse(document.getElementById('jsonData').value);
        currentCodeFlower.update(json);
    });
//    document.getElementById('jsonConverter').addEventListener('submit', function(e) {
//        e.preventDefault();
//        var origin = this.children[0].children[0].value;
//        var data = this.children[0].children[1].value;
//        var json = convertToJSON(data, origin);
//        document.getElementById('cluster_visual1_1').scrollIntoView();
//        createCodeFlower(json);
//    });

//    var cluster1 = {
//        Sex: {
//            _type: "terms",
//            terms: [{
//                term: "10대",
//                count: age10
//            }, {
//                term: "20대",
//                count: age20
//            }, {
//                term: "30",
//                count: age30
//            }]
//        }
//    };
//    $scope.cluster1 = cluster1;
}




AppListCtrl.$inject = ['$scope','$http','$resource','App', 'Min'];


function AppDetailCtrl($scope, $routeParams, App, Min) {
    Min.get_count_gender({app : $routeParams.appId}, function(d){
        var rate = d.male/(d.male+ d.female) * 100
        $scope.bar1 = [{"name":"남성("+Math.floor(rate)+"%)", "score": rate},
                       {"name":"여성("+Math.floor(100-rate)+"%)", "score": (100 - rate)}];

    });
    $scope.id = $routeParams.appId;

    $scope.app = App.get({id: $routeParams.appId}, function(app) {
        $scope.mainImageUrl = app.img;
//        var temp = app['stat'];
//        changed = temp.replace("'", "\"");
//        d = json.load(changed);
//        alert(d);


//        var copy = JSON.parser(JSON.stringify(temp));
//        alert(copy);
//        alert(copy['gender']);
        //d_ = eval(temp);
//        var obj = eval('(' +
//            temp + ')');
      //  alert(temp.ToDictionary())
//        $scope.male_ = obj.gender;
            var age10 = 80
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
                        term: "30대",
                        count: age30
                    }]
                }
            };
            $scope.results = resultsA;
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
    $scope.pro = Min.process({id_: $routeParams.appId})

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
    var date = 1341100800000; // jul 08
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


    var resultsC = {
        facets: {
            Times: {
                _type: "date_histogram",
                entries: [
                    {
                        time: 1343779200000,
                        count: temp
                    }
                    ,
                    {
                        time: 1346457600000,
                        count: 78
                    },
                    {
                        time: 1349049600000,
                        count: 45
                    },
                    {
                        time: 1351728000000,
                        count: 134
                    }
                ]
            }
        }
    };
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
    $scope.resultss = resultsC;
    $scope.resultsss = resultsC;
    var currentResults = 'A';
}


function dd(){
    {{console.log(d3.version)}}
    var w = 300,                        //width
        h = 300,                            //height
        r = 100,                            //radius
        color = d3.scale.category20c();     //builtin range of colors

    var data = [{"label":"10대", "value":20},
        {"label":"20대", "value":50},
        {"label":"30", "value":30}];

    var vis = d3.select("body")
        .append("svg:svg")              //create the SVG element inside the <body>
        .data([data])                   //associate our data with the document
        .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
        .attr("height", h)
        .append("svg:g")                //make a group to hold our pie chart
        .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
        .outerRadius(r);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
        .value(function(d) { return d.value; });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
        .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
        .attr("class", "slice");    //allow us to style things in the slices (like text)

    arcs.append("svg:path")
        .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
        .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

    arcs.append("svg:text")                                     //add a label to each slice
        .attr("transform", function(d) {                    //set the label's origin to the center of the arc
            //we have to make sure to set these before calling arc.centroid
            d.innerRadius = 0;
            d.outerRadius = r;
            return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
        })
        .attr("text-anchor", "middle")                          //center the text on it's origin
        .text(function(d, i) { return data[i].label; });        //get the label from our original data array
}