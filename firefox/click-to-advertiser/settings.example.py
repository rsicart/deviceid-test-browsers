
# in seconds
wait_before = 5

# in seconds
http_get_timeout = 5

# cookie name
cookie_name = 'adsp_di'

# domain settings
domains = {
    'first': 'advertiser.localhost',
    'third': '.adsp.localhost'
}

# target url
url = 'http://www2.adsp.localhost/click.php?id=2763-21915-5069&context-hash=e0ff593dd1fbda31689e7e1826d4e4aef0394f5a&di={}&data=&preurl='

# folder where adsp logs live, absolute path
folder_adsp_logs = '/home/user/repositories/adsp-front/sd/www2/www/data/access'

# firefox settings
firefox = {
    'profile_name': 'CookiesAll',
    'profile_folder': '/home/user/.mozilla/firefox/jl065qo8.CookiesAll', # absolute path
    'cookie_db': 'cookies.sqlite',
    'cookie_table': 'moz_cookies',
    'permission_db': 'permissions.sqlite',
    'permission_table': 'moz_perms',
}
