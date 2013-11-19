
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


    // CodeFlower
    var flowerDat;
    var currentCodeFlower;
    var createCodeFlower = function(json) {
        // update the jsonData textarea
        flowerDat = JSON.stringify(json);
        document.getElementById('jsonData').value = JSON.stringify(json);
        // remove previous flower to save memory
        if (currentCodeFlower) currentCodeFlower.cleanup();
        // adapt layout size to the total number of elements
        var total = countElements(json);
        w = parseInt(Math.sqrt(total) * 300, 10);
        h = parseInt(Math.sqrt(total) * 300, 10);
        // create a new CodeFlower
        currentCodeFlower = new CodeFlower("#cluster_visual1_1", w, h).update(json);
    };

   // d3.json('app/data/testData.json', createCodeFlower);
    d3.json('http://soma3.buzzni.com:9016/app?func=get_cluster_test', createCodeFlower);
   $scope.testCluster = Min.get_cluster_test();

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



    //
// Various accessors that specify the four dimensions of data to visualize.
    function x(d) { return d.income; }
    function y(d) { return d.lifeExpectancy; }
    function radius(d) { return d.population; }
    function color(d) { return d.region; }
    function key(d) { return d.name; }

// Chart dimensions.
    var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5},
        width = 960 - margin.right,
        height = 300;//500 - margin.top - margin.bottom;

// Various scales. These domains make assumptions of data, naturally.
    var xScale = d3.scale.log().domain([300, 1e5]).range([0, width]),
        yScale = d3.scale.linear().domain([10, 85]).range([height, 0]),
        radiusScale = d3.scale.sqrt().domain([0, 5e8]).range([0, 40]),
        colorScale = d3.scale.category10();

// The x & y axes.
    var xAxis = d3.svg.axis().orient("bottom").scale(xScale).ticks(12, d3.format(",d")),
        yAxis = d3.svg.axis().scale(yScale).orient("left");

// Create the SVG container and set the origin.
    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add the x-axis.
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

// Add the y-axis.
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

// Add an x-axis label.
    svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", width)
        .attr("y", height - 6)
        .text("인플레를 감안한 1인당 소득 (달러)");

// Add a y-axis label.
    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        .attr("y", 6)
        .attr("dy", ".75em")
        .attr("transform", "rotate(-90)")
        .text("수명 (년)");

// Add the year label; the value is set on transition.
    var label = svg.append("text")
        .attr("class", "year label")
        .attr("text-anchor", "end")
        .attr("y", height - 24)
        .attr("x", width)
        .text(1800);

// Load the data.
    d3.json("app/data/nations.json", function(nations) {

        // A bisector since many nation's data is sparsely-defined.
        var bisect = d3.bisector(function(d) { return d[0]; });

        // Add a dot per nation. Initialize the data at 1800, and set the colors.
        var dot = svg.append("g")
            .attr("class", "dots")
            .selectAll(".dot")
            .data(interpolateData(1800))
            .enter().append("circle")
            .attr("class", "dot")
            .style("fill", function(d) { return colorScale(color(d)); })
            .call(position)
            .sort(order);

        // Add a title.
        dot.append("title")
            .text(function(d) { return d.name; });

        // Add an overlay for the year label.
        var box = label.node().getBBox();

        var overlay = svg.append("rect")
            .attr("class", "overlay")
            .attr("x", box.x)
            .attr("y", box.y)
            .attr("width", box.width)
            .attr("height", box.height)
            .on("mouseover", enableInteraction);

        // Start a transition that interpolates the data based on year.
        svg.transition()
            .duration(30000)
            .ease("linear")
            .tween("year", tweenYear)
            .each("end", enableInteraction);

        // Positions the dots based on data.
        function position(dot) {
            dot .attr("cx", function(d) { return xScale(x(d)); })
                .attr("cy", function(d) { return yScale(y(d)); })
                .attr("r", function(d) { return radiusScale(radius(d)); });
        }

        // Defines a sort order so that the smallest dots are drawn on top.
        function order(a, b) {
            return radius(b) - radius(a);
        }

        // After the transition finishes, you can mouseover to change the year.
        function enableInteraction() {
            var yearScale = d3.scale.linear()
                .domain([1800, 2009])
                .range([box.x + 10, box.x + box.width - 10])
                .clamp(true);

            // Cancel the current transition, if any.
            svg.transition().duration(0);

            overlay
                .on("mouseover", mouseover)
                .on("mouseout", mouseout)
                .on("mousemove", mousemove)
                .on("touchmove", mousemove);

            function mouseover() {
                label.classed("active", true);
            }

            function mouseout() {
                label.classed("active", false);
            }

            function mousemove() {
                displayYear(yearScale.invert(d3.mouse(this)[0]));
            }
        }

        // Tweens the entire chart by first tweening the year, and then the data.
        // For the interpolated data, the dots and label are redrawn.
        function tweenYear() {
            var year = d3.interpolateNumber(1800, 2009);
            return function(t) { displayYear(year(t)); };
        }

        // Updates the display to show the specified year.
        function displayYear(year) {
            dot.data(interpolateData(year), key).call(position).sort(order);
            label.text(Math.round(year));
        }

        // Interpolates the dataset for the given (fractional) year.
        function interpolateData(year) {
            return nations.map(function(d) {
                return {
                    name: d.name,
                    region: d.region,
                    income: interpolateValues(d.income, year),
                    population: interpolateValues(d.population, year),
                    lifeExpectancy: interpolateValues(d.lifeExpectancy, year)
                };
            });
        }

        // Finds (and possibly interpolates) the value for the specified year.
        function interpolateValues(values, year) {
            var i = bisect.left(values, year, 0, values.length - 1),
                a = values[i];
            if (i > 0) {
                var b = values[i - 1],
                    t = (year - a[0]) / (b[0] - a[0]);
                return a[1] * (1 - t) + b[1] * t;
            }
            return a[1];
        }
    });









    // Scatter

    var scatterMargin = {top: 20, right: 20, bottom: 30, left: 40},
        scatterWidth = 960 - scatterMargin.left - scatterMargin.right,
        scatterHeight = 350 - scatterMargin.top - scatterMargin.bottom;

    var scatterX = d3.scale.linear()
        .range([0, scatterWidth]);

    var scatterY = d3.scale.linear()
        .range([scatterHeight, 0]);

    var scatterColor = d3.scale.category10();

    var scatterXAxis = d3.svg.axis()
        .scale(scatterX)
        .orient("bottom");

    var scatterYAxis = d3.svg.axis()
        .scale(scatterY)
        .orient("left");

    var scatterSvg = d3.select("scatter").append("svg")
        .attr("width", scatterWidth + scatterMargin.left + scatterMargin.right)
        .attr("height", scatterHeight + scatterMargin.top + scatterMargin.bottom)
        .append("g")
        .attr("transform", "translate(" + scatterMargin.left + "," + scatterMargin.top + ")");

    d3.tsv("app/data/scatterData.tsv", function(error, data) {
        data.forEach(function(d) {
            d.sepalLength = +d.sepalLength;
            d.sepalWidth = +d.sepalWidth;
        });

        scatterX.domain(d3.extent(data, function(d) { return d.sepalWidth; })).nice();
        scatterY.domain(d3.extent(data, function(d) { return d.sepalLength; })).nice();

        scatterSvg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + scatterHeight + ")")
            .call(scatterXAxis)
            .append("text")
            .attr("class", "label")
            .attr("x", scatterWidth)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text("Sepal Width (cm)");

        scatterSvg.append("g")
            .attr("class", "y axis")
            .call(scatterYAxis)
            .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Sepal Length (cm)")

        scatterSvg.selectAll(".dot")
            .data(data)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .attr("cx", function(d) { return scatterX(d.sepalWidth); })
            .attr("cy", function(d) { return scatterY(d.sepalLength); })
            .style("fill", function(d) { return scatterColor(d.species); });

        var scatterLegend = scatterSvg.selectAll(".legend")
            .data(scatterColor.domain())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        scatterLegend.append("rect")
            .attr("x", scatterWidth - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", scatterColor);

        scatterLegend.append("text")
            .attr("x", scatterWidth - 24)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function(d) { return d; });

    });






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
    $scope.pro2 = Min.process2({id_: $routeParams.appId})
//    $scope.pro3 = Min.process3({id_: $routeParams.appId})
    $scope.weekDay_new = Min.weekDay_new({id_: $routeParams.appId})

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
//    Min.date_app({id_:$routeParams.appId}, function(weekday){
//        $scope.weekday = weekday
//        var resultsB = {
//            facets: {
//                Times: {
//                    _type: "date_histogram",
//                    entries: [
//                        {
//                            time: 86400000*3,
//                            count: weekday.mon
//                        },
//                        {
//                            time: 86400000*4,
//                            count: weekday.tue
//                        },
//                        {
//                            time: 86400000*5,
//                            count: weekday.wed
//                        },
//                        {
//                            time: 86400000*6,
//                            count: weekday.thu
//                        },
//                        {
//                            time: 86400000*7,
//                            count: weekday.fri
//                        },
//                        {
//                            time: 86400000*8,
//                            count: weekday.sat
//                        },
//                        {
//                            time: 86400000*9,
//                            count: weekday.sun
//                        }
//                    ]
//                }
//            }
//        };
//        var resultsB_ = {
//            facets: {
//                Times: {
//                    _type: "date_histogram",
//                    entries: [
//                        {
//                            time: 86400000*2,
//                            count: weekday.sun
//                        },
//                        {
//                            time: 86400000*3,
//                            count: weekday.mon
//                        },
//                        {
//                            time: 86400000*4,
//                            count: weekday.tue
//                        },
//                        {
//                            time: 86400000*5,
//                            count: weekday.wed
//                        },
//                        {
//                            time: 86400000*6,
//                            count: weekday.thu
//                        },
//                        {
//                            time: 86400000*7,
//                            count: weekday.fri
//                        },
//                        {
//                            time: 86400000*8,
//                            count: weekday.sat
//                        }
//                    ]
//                }
//            }
//        };
//
//        $scope.filterSearchB = function (type, term) {
//            switch (currentResults) {
//                case 'A':
//                    $scope.results_histo = resultsB_;
//                    currentResults = 'B';
//                    break;
//                case 'B':
//                    $scope.results_histo = resultsB;
//                    currentResults = 'A';
//                    break;
//            }
//        };
//        $scope.results_histo = resultsB;
//        var currentResults = 'A';
//
//    });


//    var resultsC = {
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
//    };
//    var resultsC_ = {
////        facets: {
////            Times: {
////                _type: "date_histogram",
////                entries: [
////                    {
////                        time: 1343779200000,
////                        count: temp
////                    }
////                    ,
////                    {
////                        time: 1346457600000,
////                        count: 78
////                    },
////                    {
////                        time: 1349049600000,
////                        count: 45
////                    },
////                    {
////                        time: 1351728000000,
////                        count: 134
////                    }
////                ]
////            }
////        }
//    };
//
//    $scope.filterByDate = function (type, term) {
//        switch (currentResults) {
//            case 'A':
//                $scope.results = resultsC;
//                currentResults = 'B';
//                break;
//            case 'B':
//                $scope.results = resultsC_;
//                currentResults = 'A';
//                break;
//        }
//    };
//    $scope.resultss = resultsC;
//    $scope.resultsss = resultsC;
//    var currentResults = 'A';







    // basic bar chart

    de2 = [{'count': 728, 'name': 'sample0'}, {'count': 824, 'name': 'sample1'}, {'count': 963, 'name': 'sample2'}, {'count': 927, 'name': 'sample3'}, {'count': 221, 'name': 'sample4'}, {'count': 574, 'name': 'sample5'}, {'count': 733, 'name': 'sample6'}, {'count': 257, 'name': 'sample7'}, {'count': 879, 'name': 'sample8'}, {'count': 620, 'name': 'sample9'}];


    //$scope.weekday_de = $scope.weekDay_new;

    de = Min.weekDay_new({id_: $routeParams.appId}, function(week){

        $scope.de = week;

//        de2 = de.max()


        var mySVG = d3.select("mybarchart")
            .append("svg")
            .attr("width", 1500)
            .attr("height", 500)
//        .style('position','absolute')
//        .style('top',50)
//        .style('left',40)
            .attr('class','fig');

        var heightScale = d3.scale.linear()
            .domain([0, d3.max(de,function(d) { return d.count;})])
            .range([0, 400]);

        mySVG.selectAll(".xLabel")
            .data(de)
            .enter().append("svg:text")
            .attr("x", function(d,i) {return 128 + (i * 44);})
            .attr("y", 435)
            .attr("text-anchor", "middle")
            .text(function(d,i) {return d.name;})
            .attr('transform',function(d,i) {return 'rotate(-90,' + (128 + (i * 44)) + ',435)';});

        mySVG.selectAll(".yLabel")
            .data(heightScale.ticks(10))
            .enter().append("svg:text")
            .attr('x',80)
            .attr('y',function(d) {return 400 - heightScale(d);})
            .attr("text-anchor", "end")
            .text(function(d) {return d;});

        mySVG.selectAll(".yTicks")
            .data(heightScale.ticks(10))
            .enter().append("svg:line")
            .attr('x1','90')
            .attr('y1',function(d) {return 400 - heightScale(d);})
            .attr('x2',420)
            .attr('y2',function(d) {return 400 - heightScale(d);})
            .style('stroke','lightgray');

        var myBars = mySVG.selectAll('rect')
            .data(de)
            .enter()
            .append('svg:rect')
            .attr('width',40)
            .attr('height',function(d,i) {return heightScale(d.count);})
            .attr('x',function(d,i) {return (i * 44) + 100;})
            .attr('y',function(d,i) {return 400 - heightScale(d.count);})
            .style('fill','lightblue');


    })














    var basicMargin = {top: 20, right: 20, bottom: 30, left: 60},
        basicWidth = 960 - basicMargin.left - basicMargin.right,
        basicHeight = 400 - basicMargin.top - basicMargin.bottom;

    var parseDate = d3.time.format("%d-%b-%y").parse;


    var basicX = d3.time.scale()
        .range([0, basicWidth]);

    var basicY = d3.scale.linear()
        .range([basicHeight, 0]);

    var basicXAxis = d3.svg.axis()
        .scale(basicX)
        .orient("bottom");

    var basicYAxis = d3.svg.axis()
        .scale(basicY)
        .orient("left");

    var basicLine = d3.svg.line()
        .x(function(d) { return basicX(d.date); })
        .y(function(d) { return basicY(d.count); });

    var basicSvg = d3.select("basicChart").append("svg")
        .attr("width", basicWidth + basicMargin.left + basicMargin.right)
        .attr("height", basicHeight + basicMargin.top + basicMargin.bottom)
        .append("g")
        .attr("transform", "translate(" + basicMargin.left + "," + basicMargin.top + ")");


    date_new = Min.date_new2({id_: $routeParams.appId}, function(data){



        $scope.date_new_b = data[0].date;
        $scope.date_new_e = data[(data.length-1)].date;


        data.forEach( function(d) {
            d.date = parseDate(d.date);
            d.count = +d.count;

            $scope.parseDate2 = data;
        });

        basicX.domain(d3.extent($scope.parseDate2, function(d) { return d.date; }));
        basicY.domain(d3.extent($scope.parseDate2, function(d) { return d.count; }));

        basicSvg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + basicHeight + ")")
            .call(basicXAxis);

        basicSvg.append("g")
            .attr("class", "y axis")
            .call(basicYAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("count (명)");

        basicSvg.append("path")
            .datum(data)//$scope.parseDate2)
            .attr("class", "line")
            .attr("d", basicLine);
    });




//    basic chart



//    d3.tsv("app/data/basicChartDat.tsv", function(error, data) {
//        data.forEach(function(d) {
//            d.date = d.date;//parseDate(d.date);
//            d.close = +d.close;
//
//            //d = {"date":"2007-04-23T15:00:00.000Z","close":93.24}
////            d.date = "2007-04-23T15:00:00.000Z";
////            d.close = 93.24;
//
//            $scope.parseDate2 = data;
//        });
//
//        basicX.domain(d3.extent(data, function(d) { return d.date; }));
//        basicY.domain(d3.extent(data, function(d) { return d.close; }));
//
//        basicSvg.append("g")
//            .attr("class", "x axis")
//            .attr("transform", "translate(0," + basicHeight + ")")
//            .call(basicXAxis);
//
//        basicSvg.append("g")
//            .attr("class", "y axis")
//            .call(basicYAxis)
//            .append("text")
//            .attr("transform", "rotate(-90)")
//            .attr("y", 6)
//            .attr("dy", ".71em")
//            .style("text-anchor", "end")
//            .text("설치 수 (대)");
//
//        basicSvg.append("path")
//            .datum(data)
//            .attr("class", "line")
//            .attr("d", basicLine);
//    });













    // population

//    var popMargin = {top: 20, right: 40, bottom: 30, left: 20},
//        popWidth = 960 - popMargin.left - popMargin.right,
//        popHeight = 350 - popMargin.top - popMargin.bottom,
//        barWidth = Math.floor(popWidth / 19) - 1;
//
//    var x = d3.scale.linear()
//        .range([barWidth / 2, popWidth - barWidth / 2]);
//
//    var y = d3.scale.linear()
//        .range([popHeight, 0]);
//
//    var yAxis = d3.svg.axis()
//        .scale(y)
//        .orient("right")
//        .tickSize(-popWidth)
//        .tickFormat(function(d) { return Math.round(d / 1e6) + "M"; });
//
//// An SVG element with a bottom-right origin.
//    var svg = d3.select("svgBody").append("svg")
//        .attr("width", popWidth + popMargin.left + popMargin.right)
//        .attr("height", popHeight + popMargin.top + popMargin.bottom)
//        .append("g")
//        .attr("transform", "translate(" + popMargin.left + "," + popMargin.top + ")");
//
//// A sliding container to hold the bars by birthyear.
//    var birthyears = svg.append("g")
//        .attr("class", "birthyears");
//
//// A label for the current year.
//    var title = svg.append("text")
//        .attr("class", "title")
//        .attr("dy", ".71em")
//        .text(2000);
//
//    d3.csv("app/data/population.csv", function(error, data) {
//
//        // Convert strings to numbers.
//        data.forEach(function(d) {
//            d.people = +d.people;
//            d.year = +d.year;
//            d.age = +d.age;
//        });
//
//        // Compute the extent of the data set in age and years.
//        var age1 = d3.max(data, function(d) { return d.age; }),
//            year0 = d3.min(data, function(d) { return d.year; }),
//            year1 = d3.max(data, function(d) { return d.year; }),
//            year = year1;
//
//        // Update the scale domains.
//        x.domain([year1 - age1, year1]);
//        y.domain([0, d3.max(data, function(d) { return d.people; })]);
//
//        // Produce a map from year and birthyear to [male, female].
//        data = d3.nest()
//            .key(function(d) { return d.year; })
//            .key(function(d) { return d.year - d.age; })
//            .rollup(function(v) { return v.map(function(d) { return d.people; }); })
//            .map(data);
//
//        // Add an axis to show the population values.
//        svg.append("g")
//            .attr("class", "y axis")
//            .attr("transform", "translate(" + popWidth + ",0)")
//            .call(yAxis)
//            .selectAll("g")
//            .filter(function(value) { return !value; })
//            .classed("zero", true);
//
//        // Add labeled rects for each birthyear (so that no enter or exit is required).
//        var birthyear = birthyears.selectAll(".birthyear")
//            .data(d3.range(year0 - age1, year1 + 1, 5))
//            .enter().append("g")
//            .attr("class", "birthyear")
//            .attr("transform", function(birthyear) { return "translate(" + x(birthyear) + ",0)"; });
//
//        birthyear.selectAll("rect")
//            .data(function(birthyear) { return data[year][birthyear] || [0, 0]; })
//            .enter().append("rect")
//            .attr("x", -barWidth / 2)
//            .attr("width", barWidth)
//            .attr("y", y)
//            .attr("height", function(value) { return popHeight - y(value); });
//
//        // Add labels to show birthyear.
//        birthyear.append("text")
//            .attr("y", popHeight - 4)
//            .text(function(birthyear) { return birthyear; });
//
//        // Add labels to show age (separate; not animated).
//        svg.selectAll(".age")
//            .data(d3.range(0, age1 + 1, 5))
//            .enter().append("text")
//            .attr("class", "age")
//            .attr("x", function(age) { return x(year - age); })
//            .attr("y", popHeight + 4)
//            .attr("dy", ".71em")
//            .text(function(age) { return age; });
//
//        // Allow the arrow keys to change the displayed year.
//        window.focus();
//        d3.select(window).on("keydown", function() {
//            switch (d3.event.keyCode) {
//                case 37: year = Math.max(year0, year - 10); break;
//                case 39: year = Math.min(year1, year + 10); break;
//            }
//            update();
//        });
//
//        function update() {
//            if (!(year in data)) return;
//            title.text(year);
//
//            birthyears.transition()
//                .duration(750)
//                .attr("transform", "translate(" + (x(year1) - x(year)) + ",0)");
//
//            birthyear.selectAll("rect")
//                .data(function(birthyear) { return data[year][birthyear] || [0, 0]; })
//                .transition()
//                .duration(750)
//                .attr("y", y)
//                .attr("height", function(value) { return popHeight - y(value); });
//        }
//    });




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