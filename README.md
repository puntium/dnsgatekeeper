# dnsgatekeeper
Whitelist-based dns firewall (wrapper around dnsmasq).

I use this currently to allow-list sets of domains for my children. I originally used pihole, but found
the lack of any kind of wildcard allow-listing too much of a pain to deal with. dnsmasq only offers limited patterns (i.e. you can provide suffixes), but this handles most cases cleanly.

## How to run

You need

1. Linux machine
1. dnsmasq installed
1. Python 3. I currently run this with Python 3.5.2
1. pipenv

First build the pipenv

    pipenv lock
    pipenv sync

Then run the script

    pipenv run python3 dnsgatekeeper.py

The script will immediately try to acquire root priveleges, so you will need to type in your password.

Point the browser at your machine's IP to access the web control interface which allows you to temporarily
disable the blocking.

## Other setup

This only works if your client in questions is using the machine where you're running dnsgatekeeper as a DNS server. I do this by creating a separate vlan and wifi segment using Unifi, and handing out a custom dns server ip in the DHCP settings.

Yes, this is trivially circumventable if you know how to override your local DNS settings. But my kids are not that smart (yet).
