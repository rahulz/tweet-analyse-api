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
analyse.controller('Controller', function PhoneListController($scope, Socket) {

    Socket.socket.onMessage(function (message) {
        console.log(message.data);
    });
    $scope.generate = function () {
        Socket.send({q: $scope.q, action: "generate"});
    }
});