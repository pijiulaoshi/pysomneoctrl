#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
Somneo HTTP

USAGE: Load SomneoHttp, with or without IP.

somneo_http = SomneoHttp(ip: (optional) if Somneo has static IP, use it here.)
somneo_http._get(path: path to data needed, target: (optional) "device" or "system")
somneo_http._put(path: path to settings, payload: (dict) keys and values that need to be changed, target: (optional) "device" or "system")

"""
import requests
import urllib3
urllib3.disable_warnings()
import socket
import json
import logging
import time



MC_HOST = '239.255.255.250'
MC_PORT = 1900
MC_ST = 'urn:philips-com:device:DiProduct:1'
MC_MSG = f'M-SEARCH * HTTP/1.1\r\nHOST:{MC_HOST}:1900\r\nST:{MC_ST}\r\nMX:5\r\nMAN:"ssdp:discover"\r\n\r\n'

_LOGGER = logging.getLogger('pysomneoctrl_http')

class SomneoHttp:
    """HTTP Client for Somneo"""
    def __init__(self, ip=None, cooldown=0):
        self._to = 15
        self._rt = 8 #retries, what does this do??
        self._cd = cooldown
        self._session = requests.Session()
        self._ip = self._validateIP(ip) if ip else self._getIP()
        self._base_url = f'https://{self._ip}/di/v1/products/'
        self._system_url = f"{self._base_url}0/"
        self._device_url = f"{self._base_url}1/"
        self._headers = {"Content-Type": "application/json"}
        
    def _url(self, target, path):
        if target == "device":
            url = self._device_url + path
        elif target == "system":
            url = self._system_url + path
        return(url)

    def _get(self, path, target="device"):
        url = self._url(target, path)
        r = self._session.request('GET', url, verify=False, timeout=self._to)
        if r.status_code == 200:            
            data = r.json()
            time.sleep(self._cd)
            return(data)
        else:
            _LOGGER.error('Connection error or Invallid request')

    def _put(self, path, payload={}, target="device"):
        url = self._url(target, path)
        j_payload = json.dumps(payload)
        r = self._session.request('PUT', url, data=j_payload, headers=self._headers, verify=False, timeout=self._to)
        if r.status_code == 200:            
            data = r.json()
            time.sleep(self._cd)
            return(data)
        else:
            _LOGGER.error('Connection error or Invallid request')

    def _getIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(self._to)
        s.sendto(MC_MSG.encode(), (MC_HOST, MC_PORT) )
        try:
            while True:
                data, addr = s.recvfrom(12000)
                dev_ip = addr[0]
                return dev_ip
        except socket.timeout:
            _LOGGER.error('Connection to Somneo timed out.')

    def _validateIP(self, ip):
        try:
            url = f'https://{ip}/di/v1/products/'
            data = self._session.request('GET', url, verify=False, timeout=self._to)
            if data.status_code == 200:
                return ip
            else:
                _LOGGER.error('Invalid Somneo IP address')
        except ():
            _LOGGER.error('Invalid Somneo IP address')
