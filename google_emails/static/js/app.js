'use strict';

var app = angular.module('getEmailsApp', ['ui.bootstrap', 'angularUtils.directives.dirPagination']);

app.constant('ROUTES', {
    'emailsList': '/api/emails'
});

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[{').endSymbol('}]');
});
