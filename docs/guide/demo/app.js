/**
 * Created by Snare on 24.08.16.
 */

const EVENT_DASHBOARDS_RECEIVED = "dashboards_received";
const EVENT_DASHBOARDS_SAVED = "dashboards-saved";
const EVENT_CI_LIVE_DATA_RECEIVED = "ci_live_data_received";
const EVENT_CI_HISTORY_DATA_RECEIVED = "ci_history_data_received";
const EVENT_CIS_RECEIVED = "cis_received";
const EVENT_CI_IDS_RECEIVED = "ci_ids_received";
const EVENT_CI_CATS_RECEIVED = "ci_cats_received";
const EVENT_MEMORY_CATS_RECEIVED = "memory_cats_received";
const EVENT_DELETE_WIDGET = "delete_widget";
const EVENT_ITEM_RESIZE = "item_resize";
const EVENT_TOGGLE_EDIT_MODE = "toggle_edit_mode";
const EVENT_SAVE = "save";
const EVENT_USER_VALIDATED = "user_validated";
const EVENT_GATHERING_RATE_RECEIVED = "gathering_rate_received";
const EVENT_ALL_GATHERING_RATES_RECEIVED = "all_gathering_rates_received";
const EVENT_SET_GATHERING_RATE = "delete_gathering_rate";
const EVENT_SAVE_GATHERING_RATE = "save_gathering_rate";
const EVENT_UPDATE_GATHERING_RATE = "update_gathering_rate";
const EVENT_SLIDER_DRAG_END = "slider_drag_ended";




var app = angular.module('app',[
    'ngRoute',
    'gridster',
    'ngMaterial',
    'highcharts-ng',
    'angularViewportWatch',
    'pascalprecht.translate',
    'ngMockE2E'
]);

app.config(function($mdThemingProvider) {
    $mdThemingProvider.definePalette('black', {
        '50': '242424',
        '100': '242424',
        '200': '242424',
        '300': '242424',
        '400': '242424',
        '500': '242424',
        '600': '242424',
        '700': '242424',
        '800': '242424',
        '900': '242424',
        'A100': '242424',
        'A200': '242424',
        'A400': '242424',
        'A700': '242424',
        'contrastDefaultColor': 'light'
    });
    $mdThemingProvider.definePalette('white', {
        '50': 'ffffff',
        '100': 'ffffff',
        '200': 'ffffff',
        '300': 'ffffff',
        '400': 'ffffff',
        '500': 'ffffff',
        '600': 'ffffff',
        '700': 'ffffff',
        '800': 'ffffff',
        '900': 'ffffff',
        'A100': 'ffffff',
        'A200': 'ffffff',
        'A400': 'ffffff',
        'A700': 'ffffff',
        'contrastDefaultColor': 'dark'
    });
    $mdThemingProvider.definePalette('blue', {
        '50': '00b8d4',
        '100': '00b8d4',
        '200': '00b8d4',
        '300': '00b8d4',
        '400': '00b8d4',
        '500': '00b8d4',
        '600': '00b8d4',
        '700': '00b8d4',
        '800': '00b8d4',
        '900': '00b8d4',
        'A100': '00b8d4',
        'A200': '00b8d4',
        'A400': '00b8d4',
        'A700': '00b8d4',
        'contrastDefaultColor': 'light'
    });

    $mdThemingProvider.theme('default')
        .primaryPalette('black')
        .backgroundPalette('white')
        .accentPalette('blue')
        .dark();
});

//HIGHCHARTS OPTIONS
app.config(function(){


    /**
     * Dark theme for Highcharts JS
     * @author Torstein Honsi
     */

// Load the fonts
    Highcharts.createElement('link', {
        href: 'https://fonts.googleapis.com/css?family=Unica+One',
        rel: 'stylesheet',
        type: 'text/css'
    }, null, document.getElementsByTagName('head')[0]);

    Highcharts.theme = {
        colors: ["#2b908f", "#90ee7e", "#f45b5b", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
            "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
        chart: {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
                stops: [
                    [0, '#2a2a2b'],
                    [1, '#3e3e40']
                ]
            },
            style: {
                fontFamily: "'Unica One', sans-serif"
            },
            plotBorderColor: '#606063'
        },
        title: {
            style: {
                color: '#E0E0E3',
                textTransform: 'uppercase',
                fontSize: '20px'
            }
        },
        subtitle: {
            style: {
                color: '#E0E0E3',
                textTransform: 'uppercase'
            }
        },
        xAxis: {
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            title: {
                style: {
                    color: '#A0A0A3'

                }
            }
        },
        yAxis: {
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            tickWidth: 1,
            title: {
                style: {
                    color: '#A0A0A3'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            style: {
                color: '#F0F0F0'
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    color: '#B0B0B3'
                },
                marker: {
                    lineColor: '#333'
                }
            },
            boxplot: {
                fillColor: '#505053'
            },
            candlestick: {
                lineColor: 'white'
            },
            errorbar: {
                color: 'white'
            }
        },
        legend: {
            itemStyle: {
                color: '#E0E0E3'
            },
            itemHoverStyle: {
                color: '#FFF'
            },
            itemHiddenStyle: {
                color: '#606063'
            }
        },
        credits: {
            style: {
                color: '#666'
            }
        },
        labels: {
            style: {
                color: '#707073'
            }
        },

        drilldown: {
            activeAxisLabelStyle: {
                color: '#F0F0F3'
            },
            activeDataLabelStyle: {
                color: '#F0F0F3'
            }
        },

        navigation: {
            buttonOptions: {
                symbolStroke: '#DDDDDD',
                theme: {
                    fill: '#505053'
                }
            }
        },

        // scroll charts
        rangeSelector: {
            buttonTheme: {
                fill: '#505053',
                stroke: '#000000',
                style: {
                    color: '#CCC'
                },
                states: {
                    hover: {
                        fill: '#707073',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    },
                    select: {
                        fill: '#000003',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    }
                }
            },
            inputBoxBorderColor: '#505053',
            inputStyle: {
                backgroundColor: '#333',
                color: 'silver'
            },
            labelStyle: {
                color: 'silver'
            }
        },

        navigator: {
            handles: {
                backgroundColor: '#666',
                borderColor: '#AAA'
            },
            outlineColor: '#CCC',
            maskFill: 'rgba(255,255,255,0.1)',
            series: {
                color: '#7798BF',
                lineColor: '#A6C7ED'
            },
            xAxis: {
                gridLineColor: '#505053'
            }
        },

        scrollbar: {
            barBackgroundColor: '#808083',
            barBorderColor: '#808083',
            buttonArrowColor: '#CCC',
            buttonBackgroundColor: '#606063',
            buttonBorderColor: '#606063',
            rifleColor: '#FFF',
            trackBackgroundColor: '#404043',
            trackBorderColor: '#404043'
        },

        // special colors for some of the
        legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
        background2: '#505053',
        dataLabelsColor: '#B0B0B3',
        textColor: '#C0C0C0',
        contrastTextColor: '#F0F0F3',
        maskColor: 'rgba(255,255,255,0.3)'
    };

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);
});

app.config(function ($translateProvider) {
    // $translateProvider.useStaticFilesLoader({
    //     prefix: 'lang-',
    //     suffix: '.json'
    // });
    //
    // $translateProvider.preferredLanguage('de_DE')

    // bower install angular-translate-loader-static-files --save


    $translateProvider.translations('en_EN', {
        APP_HEADLINE:                       'OpServ',
        SIDENAV_OPTION_DASHBOARD_SETTINGS:  'edit Settings',
        SIDENAV_OPTION_ADD_WIDGET:          'add Widget',
        LOGIN_TEXT:                         'Login',
        LOGIN_PASSWORD_TEXT:                'Password',
        LOGIN_USERNAME_TEXT:                'Username (opserv)',
        ERROR_LOGIN_PASSWORD_TEXT:          'Wrong Password',
        ERROR_LOGIN_USERNAME_TEXT:          'Wrong Username',
        GATHERING_SETTINGS_TEXT:            'Gathering Settings',
        DASHBOARD_SETTINGS_TEXT:            'Dashboard Settings',
        WIDGET_SETTINGS_TEXT:               'Widget Settings',
        GATHERING_RATE_TEXT:                'Gathering Rate',
        CANCEL_TEXT:                        'Cancel',
        SAVE_TEXT:                          'Save',
        TITLE_TEXT:                         'Title',
        URL_TEXT:                           'URL',
        LANGUAGE_TEXT:                      'Language',
        TYPE_TEXT:                          'Type',
        EXIT_TEXT:                          'Exit',
        BACK_TEXT:                          'Back'

    });

    $translateProvider.translations('de_DE', {
        APP_HEADLINE:                       'OpServ',
        SIDENAV_OPTION_DASHBOARD_SETTINGS:  'Einstellungen ändern',
        SIDENAV_OPTION_ADD_WIDGET:          'Widget hinzufügen',
        LOGIN_TEXT:                         'Login',
        LOGIN_PASSWORD_TEXT:                'Passwort',
        LOGIN_USERNAME_TEXT:                'Benutzername (opserv)',
        ERROR_LOGIN_PASSWORD_TEXT:          'falsches Passwort',
        ERROR_LOGIN_USERNAME_TEXT:          'falscher Benutzername',
        GATHERING_SETTINGS_TEXT:            'Abtastraten einstellen',
        DASHBOARD_SETTINGS_TEXT:            'Dashboard Einstellungen',
        WIDGET_SETTINGS_TEXT:               'Widget Einstellungen',
        GATHERING_RATE_TEXT:                'Abtastrate',
        CANCEL_TEXT:                        'Abbrechen',
        SAVE_TEXT:                          'Speichern',
        TITLE_TEXT:                         'Titel',
        URL_TEXT:                           'URL',
        LANGUAGE_TEXT:                      'Sprache',
        TYPE_TEXT:                          'Typ',
        EXIT_TEXT:                          'Schließen',
        BACK_TEXT:                          'Zurück'
    });

    $translateProvider.useSanitizeValueStrategy('escapeParameters');
    $translateProvider.preferredLanguage('en_EN')
});

app.run(function($rootScope, $location, authService, $translate, $http, $httpBackend) {

    // define if need Mockup
    //opserv.org
    //docs/guide/demo

    if(window.location.host == "opserv.org"){
        $rootScope.isMock = true;
        console.log($rootScope.isMock)
    }else{
        $rootScope.isMock = false;
    }

    $rootScope.languages = [
        {label:"Deutsch", key:'de_DE'},
        {label:"English", key:'en_EN'}
    ];

    var languageKey = localStorage.getItem('language');
    if(languageKey){
        $rootScope.selectedLanguageKey = languageKey;
    }else{
        languageKey = 'en_EN';
        $rootScope.selectedLanguageKey = 'en_EN';
    }
    $translate.use(languageKey);

    var password = localStorage.getItem('password');
    var userName = localStorage.getItem('userName');
    if (password && userName){
        var encodedString = base64Encoding(userName+":"+password);
        $http.defaults.headers.common ={
            'Authorization':'Basic '+encodedString
        };
    }

    function base64Encoding(str) {
        return btoa(str)
    }

    // wird beim refresh oder wechsel einer URL aufgerunfen
    $rootScope.$on('$locationChangeStart', function() {
        var password = localStorage.getItem('password');
        var userName = localStorage.getItem('userName');
        if ((userName && password) || $rootScope.isMock ) {
            if (!authService.isLoggedIn()) {
                $location.path('/login'); // relocate for Login
            } else {
                // password und username und LoggedIn also alles gut
            }
        }else{
            $location.path('/login');
        }
    });

    /**
     * Demo MockUp
     * */

    //Dashboards
    $httpBackend.whenGET('/mock/api/preferences/current/dashboards').respond(getDemoDashboard);

    //CI DATA
    $httpBackend.whenGET('http://localhost:31337/mock/api/data/current').respond(getCIs);
    $httpBackend.whenGET(/http:\/\/localhost:31337\/mock\/api\/data\/current\/[^\/]+$/).respond(getIds);
    $httpBackend.whenGET(/http:\/\/localhost:31337\/mock\/api\/data\/current\/[^\/]+\/[^\/]+$/).respond(getCategories);
    $httpBackend.whenPUT(/http:\/\/localhost:31337\/mock\/api\/data\/current\/[^\/]+\/[^\/]+\/[^\/]+$/).respond(getCIHistoryData); //For GatheringRate
    $httpBackend.whenGET(/http:\/\/localhost:31337\/mock\/api\/data\/current\/[^\/]+\/[^\/]+\/[^\/?]+$/).respond(getCIHistoryData); //For GatheringRate
    $httpBackend.whenGET(/http:\/\/localhost:31337\/mock\/api\/data\/current\/[^\/]+\/[^\/]+\/[^\/]+?realtime=true/).respond(getCILiveData); // Live-Data

    //PassThrough
    $httpBackend.whenGET(shallPass).passThrough(); // Requests for templates are handled by the real server
    $httpBackend.whenPUT(shallPass).passThrough(); // Requests for templates are handled by the real server

    function shallPass(url) {
        return !url.includes('mock');
    }

    function getDemoDashboard() {
        var defaultWidgets = [
            { id: 0, sizeX: 15, sizeY: 10, row: 0, col: 0, displayItem: {ci: 'cpus', id: 0, category: 'usage', title:"CPUS 0 USAGE ", displayAsChart:true, realtime:true, samplingRate:1000}}
        ];
        var dashboards=[
            { title: 'Demo Monitor',widgets:defaultWidgets, baseUrl: 'http://localhost:31337/mock'} // https://397b6935.ngrok.io
        ];
        return [200,{data:{value:dashboards}},{}];

    }

    function getCIHistoryData(method, url, data) {
        var returnObject = {data:{value:[],gathering_rate: 1000}};
        for(var i =1;i<11;i++){
            var dataObject={
                avg: 5.124*i,
                timestamp: new Date().getTime()+(10000*i),
                max: 8.2344*i,
                min: 2.6564*i
            };

             returnObject.data.value.push(dataObject);
        }
        return [200,returnObject,{}];
    }
    
    function getCILiveData(method, url, data) {
        var dataObject={
            value: Math.random()*25,
            timestamp: new Date().getTime()
        };
        return [200,{data:dataObject},{}];
    }

    function getCIs() {
        var returnObject = {
            data: {},
            links: {
                children: [
                    {
                        href: "http://localhost:31337/api/data/current/cpus",
                        name: "cpu entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/cpu-cores",
                        name: "cpu core entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/gpus",
                        name: "gpu entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/disks",
                        name: "disk entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/memory",
                        name: "memory entity"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/networks",
                        name: "network entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/partitions",
                        name: "partition entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/processes",
                        name: "process entities"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/system",
                        name: "system components"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/gathering-rates",
                        name: "gathering rate overview"
                    }
                ]
            }
        };
        return [200,returnObject,{}];
    }

    function getIds() {
        var returnObject = {
            data: {},
            links: {
                children: [
                    {
                        href: "http://localhost:31337/api/data/current/cpus/0",
                        name: "cpu entity"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/cpus/1",
                        name: "cpu entity"
                    },
                    {
                        href: "http://localhost:31337/api/data/current/cpus/2",
                        name: "cpu entity"
                    }
                ]
            }
        };
        return [200,returnObject,{}];
    }

    function getCategories(method, url, data) {

        var returnObject ={};
        var cutInArray = url.split("/");
        var lastButOneItem = cutInArray[cutInArray.length-2];

        switch (lastButOneItem){
            case "cpus":
                returnObject = getForCPUS();
                break;
            case "cpu-cores":
                returnObject = getForCPUCORES();
                break;
            case "gpus":
                returnObject = getForGPUS();
                break;
            case "disks":
                returnObject = getForDisks();
                break;
            case "memory":
                returnObject = getForMemory();
                break;
            case "networks":
                returnObject = getForNetworks();
                break;
            case "partitions":
                returnObject = getForPartitions();
                break;
            case "processes":
                returnObject = getForProcesses();
                break;
        }

        function getForCPUCORES() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/usage",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForCPUS() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/usage",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForGPUS() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/temperature",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForDisks() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/temperature",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForMemory() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/used",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForPartitions() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/used",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForNetworks() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/transmitpersec",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        function getForProcesses() {
            return {
                data: {
                },
                links: {
                    children: [
                        {
                            href: "http://localhost:31337/api/data/current/cpus/0/cpuusage",
                            name: "cpu usage measurement"
                        }
                    ]
                }
            }
        }

        return [200,returnObject,{}];
    }

});

app.config(function ($routeProvider) {
    //TODO enable authentification
    $routeProvider.when("/",{
        templateUrl: "views/dashboards.html",
        name: "Dashboards",
        controller: 'DashboardCtrl'
    }).when("/login",{
        templateUrl: "views/login.html",
        name: "Login",
        controller: 'LoginCtrl'
    }).otherwise({
        redirectTo: "/"
    });
});

app.config(['$httpProvider', function($httpProvider) {

    $httpProvider.defaults.useXDomain = true;

    delete $httpProvider.defaults.headers.common['X-Requested-With'];

}

]);
