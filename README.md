# SmartHomeProject_BorderRouter
This is repository contains Border Router part of Smart Home Project.


How To configure your RapsberryPi as a WIFI Access Point:

1. Install two deamons: hosapd and dnsmasqd:

        sudo apt-get install hostapd
        sudo apt-get install dnsmasq
2.  Stop installed deamons:

        sudo systemctl stop hostapd
        sudo systemctl stop dnsmasq
        
3. Edit /etc/dhcpd.conf file with "static ip" config for WIFI interface (wlan0 in most cases)
    Add following lines at the end of file:
    
        interface wlan0
        static ip_address=192.168.0.10/24
        denyinterfaces eth0
    
4. Edit /etc/dnsmasq.conf file:
    It is good to have backup so first of all run:
    
        sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
    Then:

        sudo nano /etc/dnsmasq.conf

    File should looks like i.e.:

        expand-hosts
        interface=wlan0
        dhcp-authoritative
        dhcp-range=192.168.1.11,192.168.1.30,255.255.255.0,24h
        
5. Edit /etc/hostapd/hostapd.conf file:
    Type:

        sudo nano /etc/hostapd/hostapd.conf

    File should looks like i.e.:
    
        interface=wlan0
        hw_mode=g
        channel=7
        wmm_enabled=0
        macaddr_acl=0
        auth_algs=1
        ignore_broadcast_ssid=0
        wpa=2
        wpa_key_mgmt=WPA-PSK
        wpa_pairwise=TKIP
        rsn_pairwise=CCMP
        ssid=example_network_name
        wpa_passphrase=example_password

6. Edit /etc/network/interfaces file:
    Type:
    
        sudo nano /etc/network/interfaces
        
    Settings for wlan0 should be l.e.:
    
        auto wlan0
        allow-hotplug wlan0
        iface wlan0 inet static
        address 192.168.1.1
        netmask 255.255.255.0
