# Test device id behavior


## Requirements

* Ubuntu/debian environment
* python3
* Mozilla Firefox
* Chromium
* running adsp-front (to ckeck logs), including database


## Setup publisher webiste

* sample publisher webiste with an Ad tag (an html file with the tag it's ok)

```
<html>
<head>
        <title>Publisher</title>
</head>
<body>
        <h1>Publisher</h1>

        <!-- website test -->
        <script type="text/javascript" src="http://www2.adsp.localhost/advertise.php?live-test=true&website-id=5069&campaign-id=2763&ad-asset-id=21915&type=10&width=160&height=600&action=unique"></script>
</body>
</html>
```

* sample domain in `/etc/hosts` for publisher webiste, e.g. `127.0.0.1 publisher.localhost`
* copy that file above on your webserver setup webserver's config with a virtualhost for the sample domain added into `/etc/hosts`


## Setup advertiser website

* sample advertiser webiste with a `tracker.js` library and a tracking request

```
<html>
<head>
        <title>Advertiser</title>
</head>
<body>
        <h1>Advertiser</h1>

        <!-- synchronous -->
        <!--
        <script type="text/javascript" src="//js.adsp.localhost/tracker.js"></script>
        -->

        <!-- Adsp - Master tag - To include before </head> -->
        <script type="text/javascript">
                (function(d, w) {
                var e = d.createElement("script"), s = d.getElementsByTagName("script")[0], p = d.location.protocol === 'https:' ? 'https:' : 'http:';
                e.type = "text/javascript"; e.async = true; e.src = p + "//js.adsp.localhost/tracker.js";
                s.parentNode.insertBefore(e, s);
                w._adspq = w._adspq || [];
                })(document, window);
        </script>
        <!-- / End of Master tag -->


        <!-- Adsp - Event tag - Leads - Javascript -->
        <script type="text/javascript">
                function track(type) {
                        var userId = 'user-' + (Math.random() * 10000000000000000);
                        _adspq.push(["trackEvent", {
                        _trackerId: 87,
                        type: "inscription",
                        userId: userId 
                        }]);
                }
        </script>
        <!-- / End of Event tag -->


        <input id='btnMakeLead' type="button" value="Make a lead" onClick="track('inscription');"/>

        <!-- For automated tests, make a lead -->
        <script type="text/javascript">
                track('inscription');
        </script>
</body>
</html>
```

* sample domain in /etc/hosts for advertiser website, e.g. `127.0.0.1 advertiser.localhost`
* copy that file above on your webserver setup webserver's config with a virtualhost for the sample domain added into `/etc/hosts`


## Create a Firefox profile

* Launch Firefox a first time to create a testing profile

`firefox -P`

* Find the created profile in `~/.mozilla/firefox/` and write down the full path, you will need it later to setup settings file


## Setup settings file

* Copy `settings.example.py` to `settings.py`
* Edit `settings.py` file to match your local folders


## Launch tests

```
find . -name "test_accepts_*.py" -exec bash -c "python3 {} ; sleep 1;" \;
```
