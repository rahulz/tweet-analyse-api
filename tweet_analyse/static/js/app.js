analyse = angular.module('analyse', ['ngWebSocket']);

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
    $http.get('/trends').then(function (data) {
        $scope.trends = data.data;
    });

    Socket.socket.onMessage(function (message) {
        $scope.status = JSON.parse(message.data);
        console.log($scope.status.label);
        if ($scope.status.progress === 100) {
            $timeout(function () {
                $scope.result = $scope.status.result;
                console.log($scope.result.sentiment.counts);

                // document.getElementsByTagName('body')[0].style.backgroundImage = "url(" + $scope.result.wordcloud + ")"
                $scope.status = undefined;
                var ctx = document.getElementById('canvas').getContext('2d');
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
                    options: {}
                });
            }, 1000)
        }
    });
    $scope.generate = function () {
        $scope.result = undefined;
        console.log("init");
        Socket.send({q: $scope.q, action: "generate"});
    }
});