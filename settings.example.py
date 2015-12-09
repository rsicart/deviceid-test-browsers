
# in seconds
wait_before = 2

# in seconds
# time to wait after browser close, to give time to browser to write cookies to database
wait_after = 3

# in seconds
http_get_timeout = 5

# cookie name
cookie_name = 'adsp_di'

# folder where adsp logs live, absolute path
folder_adsp_logs = '/home/user/repositories/adsp-front/sd/www2/www/data/access'

# domain and url settings
publisher = {
    'domains': {
        'first': 'publisher.localhost',
        'third': '.adsp.localhost'
    },
    'url': 'http://publisher.localhost/publisher.html',
}

click_to_advertiser = {
    'domains': {
        'first': 'advertiser.localhost',
        'third': '.adsp.localhost'
    },
    'url': 'http://www2.adsp.localhost/click.php?id=2763-21915-5069&context-hash=e0ff593dd1fbda31689e7e1826d4e4aef0394f5a&di={}&data=&preurl=',
}

# firefox settings
firefox = {
    'profile_name': 'CookiesAll',
    'profile_folder': '/home/user/.mozilla/firefox/jl065qo8.CookiesAll', # absolute path
    'cookie_db': 'cookies.sqlite',
    'cookie_table': 'moz_cookies',
    'permission_db': 'permissions.sqlite',
    'permission_table': 'moz_perms',
}

# chromium settings
chromium = {
    'profile_name': 'Default',
    'profile_folder': '/tmp/test_chromium_1', # absolute path
    'cookie_db': 'Cookies',
    'cookie_table': 'cookies',
}
