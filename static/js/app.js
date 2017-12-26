var ev = angular.module("myApp", ["ngRoute", 'ui.bootstrap']);
ev.config(['$routeProvider', function($routeProvider) {
    $routeProvider
            .when("/main", {
                templateUrl: "/static/html/principal.htm"
            })
            .when("/contato", {
                templateUrl: "contato.htm"
            })
            .when("/inscricao", {
                templateUrl: "inscricao.htm"
            })
            .when("/cadastrarse", {
                templateUrl: "novousuario.html"
            })
            .when("/programacao", {
                templateUrl: "/static/html/programacao.html"
            })
            .when("/prazos", {
                templateUrl: "/static/html/prazos.html"
            })
            .when("/hoteis", {
                templateUrl: "/static/html/hoteis.html"
            })
            .when("/mudarsenha", {
                templateUrl: "mudarsenha.html"
            })
            .when("/perfil", {
                templateUrl: "profile.html"
            })
            .when("/questionario", {
                templateUrl: "questinscricaoevento.html"
            })
            .when("/rendermatricula", {
                templateUrl: "/static/html/matricula.html"
            })
            .when("/publico", {
                templateUrl: "/static/html/publico.html"
            })
            .when("/areainscrito", {
                templateUrl: "/areainscrito.html"
            })
            .when("/areaadmin", {
                        templateUrl: "/areaadmin.html"
            })
            .otherwise({
                redirectTo: '/main'
            });
    //$locationProvider.html5Mode(true);
}]);

ev.controller('CarouselDemoCtrl', function($scope) {
    $scope.myInterval = 3000;
    $scope.slides = [

        {
            image: 'static/img/maxresdefault.jpg'
        },
         {
            image: 'static/img/cartaz.jpg'
        },
        {
            image: 'static/img/maxresdefault2.jpg'
        },
        {
            image: 'static/img/maxresdefault3.jpg'
        },
        {
            image: 'static/img/maxresdefault4.jpg'
        }
    ];
});

ev.controller('controle2', function($scope) {
        $scope.records = [
            "Alfreds Futterkiste",
            "Berglunds snabbköp",
            "Centro comercial Moctezuma",
            "Ernst Handel"
        ]
});

ev.controller('HeaderController', function($scope, $location) {
        $scope.isActive = function (viewLocation) {
            console.log(viewLocation);
            if (viewLocation == 'dropdown')
                if ($location.path() =="/programacao" || $location.path() == '/inscricao' || $location.path() == '/prazos')
                    return true;

            if (viewLocation == 'insarea')
                if ($location.path() =="/perfil" || $location.path() == '/questionario' || $location.path() == '/areainscrito')
                    return true;


            return viewLocation === $location.path();
        };
});

//var userApp = angular.module("userApp", ["reCAPTCHA"]);

ev.controller('criarUser', function($scope) {
    $scope.criarUsuario = function(form)
    {
        // Verifica se todos os campos são válidos
        console.log("Valido: "+ $scope.nomecompleto);
        console.log("Nome completo: "+ form.nomecompleto.$valid);

        // A parte de verificacao do captcha será feito somente pelo servidor
        if(form.$valid ) {
            if ($scope.cfsenha == $scope.senha) {
                console.log("A senha é igual");
                
            }
            else {
                console.log('As senhas não são iguais');
                $scope.senha="";
                $scope.cfsenha="";

                return;
            }
        }
    };
});