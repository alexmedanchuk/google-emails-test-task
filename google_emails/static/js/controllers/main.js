'use strict';


angular.module('getEmailsApp')
.controller('MainCtrl', ['$http', '$window', 'ROUTES', function ($http, $window, ROUTES) {
    var self = this;
    self.emails = [];

    self.retrieve = function () {
        self.loading = true;
        $http({ 'method': 'GET', 'url': ROUTES.emailsList })
        .then(
            function (emails) {
                self.emails = emails.data;
                self.loaded = true;
                self.loading = false;
            },
            function (err) {
                self.loading = false;
                if (err.status === 403) {
                    $window.location.href = '/logout';
                } else {
                    self.error = 'Could not retrieve your emails. Try to relogin, please.';
                }
            }
        );
    };

    self.retrieve();
}]);