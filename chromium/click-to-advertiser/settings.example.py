
# in seconds
wait_before = 2

# time to wait after browser close, to give time to browser to write cookies to database
wait_after = 2

# in seconds
http_get_timeout = 2

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
folder_adsp_logs = '/home/user/Repo/adsp-front/sd/www2/www/data/access'

# chromium settings
chromium = {
    'profile_name': 'Default',
    'profile_folder': '/tmp/test_chromium_1', # absolute path
    'cookie_db': 'Cookies',
    'cookie_table': 'cookies',
}
