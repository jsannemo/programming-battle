
var battle = angular.module('battle', [
    'ngRoute'
]);

battle.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/app/partials/front/index.html',
            controller: 'IndexController'
        })
        .when('/login', {
            templateUrl: 'static/app/partials/team/login.html',
            controller: 'LoginController',
        })
        .when('/problems', {
            templateUrl: 'static/app/partials/problem/list.html',
            controller: 'ProblemsListController',
        })
        .when('/problem/:problemTag', {
            templateUrl: 'static/app/partials/problem/view.html',
            controller: 'ProblemViewController',
        })
        .otherwise({
            templateUrl: 'static/app/partials/front/404.html',
            controller: 'IndexController'
        });
}]);

battle.controller('BattleController', function ($scope) {
    $scope.logged_in = false;
    $scope.author = null;
    // $scope.logged_in = true;
    // $scope.author = {
    //     'username': 'Test123',
    //     'role': 'coder',
    //     'team': {
    //         'name': 'Meow'
    //     }
    // };
    $scope.errors = [];
    $scope.contest = {
        'name': 'Test Contest',
        'is_started': function () {
            return true;
        },
        'is_running': function () {
            return true;
        },
        'is_finished': function () {
            return false;
        },
        'start_time': new Date(),
        'get_end_time': function () {
            return new Date();
        },
        'get_elapsed_str': function () {
            return '00:30';
        },
        'get_remaining_str': function () {
            return '00:30';
        },
        'get_progress': function () {
            return '50';
        },
        'get_until_start_str': function () {
            return '';
        }
    };
});


battle.controller('IndexController', function ($scope) {

});


battle.controller('LoginController', function ($scope) {
    $scope.credentials = {
        'username': '',
        'password': ''
    };

    $scope.performLogin = function (credentials) {
        console.log('logging in with ' + credentials.username + ' and ' + credentials.password);
    };

});


battle.factory('ProblemsFactory', function () {
    var factory = {};

    factory.problems = [];

    factory.problems.push({
        'is_available': function () {
            return true;
        },
        'get_letter': function () {
            return 'A';
        },
        'tag': 'meow',
        'name': 'Problem A',
        'solutions': [],
        'testcases': [],
        'available_from': '00:00',
        'statement': '<p>This is <b>Problem A</b>. Test meow</p>'
    });

    factory.problems.push({
        'is_available': function () {
            return true;
        },
        'get_letter': function () {
            return 'B';
        },
        'tag': 'moo',
        'name': 'Problem B',
        'solutions': [],
        'testcases': [],
        'available_from': '00:20',
        'statement': '<p>This is <b>Problem B</b>. Test meow</p>'
    });

    factory.problems.push({
        'is_available': function () {
            return false;
        },
        'get_letter': function () {
            return 'C';
        },
        'tag': 'woof',
        'name': 'Problem C',
        'solutions': [],
        'testcases': [],
        'available_from': '00:40',
        'statement': '<p>This is <b>Problem C</b>. Test meow</p>'
    });

    return factory;
});


battle.controller('ProblemsListController', function ($scope, ProblemsFactory) {
    $scope.problems = ProblemsFactory.problems;
});


battle.controller('ProblemViewController', function ($scope, $routeParams, $sce, ProblemsFactory) {
    $scope.problem = $.grep(ProblemsFactory.problems, function (p) {
        return p.tag == $routeParams.problemTag;
    })[0];

    $scope.problem_statement = $sce.trustAsHtml($scope.problem.statement);
});

