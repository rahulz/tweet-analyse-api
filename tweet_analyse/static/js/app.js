analyse = angular.module('analyse', ['ngWebSocket', 'ui.grid']);

analyse.factory('Socket', function ($websocket) {
    var dataStream = $websocket('ws://' + window.location.host + '/ws');
    var collection = [];
    var methods = {
        collection: collection,
        socket: dataStream,
        send: function (data) {

            dataStream.send(data)
        }
    };
    return methods;
});
analyse.controller('Controller', function PhoneListController($scope, $timeout, $http, Socket) {
    // $('.overlay').show();

    $http.get('/trends').then(function (data) {
        $scope.trends = data.data;
    });
    $scope.tweetGridOptions = {
        enableSorting: true,
        columnDefs: [
            {field: 'created_at'},
            {field: 'id'},
            {field: 'text'},
            {field: 'user.name', name: 'User'},
            {field: 'retweeted_status.retweet_count', name: 'Retweet count'},
            {field: 'retweeted_status.favorite_count', name: 'Favorite count'},


        ]
    };

    Socket.socket.onMessage(function (message) {
        $scope.status = JSON.parse(message.data);
        console.log($scope.status.label);
        if ($scope.status.progress === 100) {
            $timeout(function () {
                $scope.result = $scope.status.result;
                console.log($scope.result.tweets);

                // document.getElementsByTagName('body')[0].style.backgroundImage = "url(" + $scope.result.wordcloud + ")"
                $scope.status = undefined;
                var ctx = document.getElementById('canvas').getContext('2d');
                $scope.tweetGridOptions.data = $scope.result.tweets;
                var myChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ["Positive", "Negative", "Neutral"],
                        datasets: [{
                            data: $scope.result.sentiment.counts,
                            backgroundColor: [
                                "#0a54b1",
                                "#fa1d54",
                                "#597683"
                            ], borderWidth: [0, 0, 0]
                        }
                        ]
                    },
                    options: {
                        legend: {
                            labels: {
                                defaultFontFamily: 'Roboto'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Sentiment analysis: ' + $scope.q
                        }
                    }
                });
            }, 1000)
        }
    });
    $scope.generate = function (q) {
        if (q)
            $scope.q = q;
        $scope.result = undefined;
        console.log("init");
        Socket.send({q: $scope.q, action: "generate"});
    }
    $('.overlay').slideUp('fast', function () {
        $('.overlay').css({'opacity': 1});

    });
});