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
const EVENT_USER_VALIDATED = "user-validated";



var app = angular.module('app',[
    'ngRoute',
    'gridster',
    'ngMaterial',
    'highcharts-ng',
    'angularViewportWatch',
    'pascalprecht.translate'
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
        LOGIN_SECRET_TEXT:                  'Secret (opserv)',
        ERROR_LOGIN_SECRET_TEXT:            'Wrong Secret',
        OPSERV_SETTINGS_TEXT:               'OpServ Settings',
        DASHBOARD_SETTINGS_TEXT:            'Dashboard Settings',
        WIDGET_SETTINGS_TEXT:               'Widget Settings',
        GATHERING_RATE_TEXT:                'Gathering Rate',
        CANCEL_TEXT:                        'Cancel',
        SAVE_TEXT:                          'Save',
        TITLE_TEXT:                         'Title',
        URL_TEXT:                           'URL',
        LANGUAGE_TEXT:                      'Language',
        TYPE_TEXT:                          'Type'
    });

    $translateProvider.translations('de_DE', {
        APP_HEADLINE:                       'OpServ',
        SIDENAV_OPTION_DASHBOARD_SETTINGS:  'Einstellungen ändern',
        SIDENAV_OPTION_ADD_WIDGET:          'Widget hinzufügen',
        LOGIN_TEXT:                         'Login',
        LOGIN_SECRET_TEXT:                  'Passwort (opserv)',
        ERROR_LOGIN_SECRET_TEXT:            'falsches Passwort',
        OPSERV_SETTINGS_TEXT:               'OpServ Einstellungen',
        DASHBOARD_SETTINGS_TEXT:            'Dashboard Einstellungen',
        WIDGET_SETTINGS_TEXT:               'Widget Einstellungen',
        GATHERING_RATE_TEXT:                'Abtastrate',
        CANCEL_TEXT:                        'Abbrechen',
        SAVE_TEXT:                          'Speichern',
        TITLE_TEXT:                         'Titel',
        URL_TEXT:                           'URL',
        LANGUAGE_TEXT:                      'Sprache',
        TYPE_TEXT:                          'Typ'
    });

    $translateProvider.useSanitizeValueStrategy('escapeParameters');
    $translateProvider.preferredLanguage('en_EN')
});

app.run(function($rootScope, $location, authService, $translate) {

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

    // wird beim refresh oder wechsel einer URL aufgerunfen
    $rootScope.$on('$locationChangeStart', function() {
        var secret = localStorage.getItem('secret');
        if (secret) {
            if (!authService.isLoggedIn()) {
                $location.path('/login'); // relocate for Login
            } else {
                $location.path('/'); // secret und LoggedIn also alles gut
            }
        }else{
            $location.path('/login');
        }
    });
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

app.config(['$httpProvider', function($httpProvider, authService) {

    var secret = localStorage.getItem('secret');
    console.log(secret);
    var encodedString = base64Encoding(secret);

    $httpProvider.defaults.headers.common ={
        'Authorization':'Basic '+secret
    };

    $httpProvider.defaults.useXDomain = true;

    delete $httpProvider.defaults.headers.common['X-Requested-With'];


    function base64Encoding(str) {
        return btoa(encodeURIComponent('dgfchvmb').replace(/%([0-9A-F]{2})/g,function (match, p1) {
            return String.fromCharCode('0x'+p1);
        }))
    }
}

]);
