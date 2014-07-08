#!python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 lefebvre <lefebvre@lefebvre-XPS>
#
# Distributed under terms of the MIT license.

"""
Expose a local lxc machine(port) on the public network via the host machine
"""

import lxc
import netifaces
import os


def get_containers():
    containersNames = lxc.list_containers(active=True)
    containers = []
    for containerName in containersNames:
        container = lxc.Container(containerName)
        if container.running:
            containers.append(container)

    return containers


def get_active_ips():
    activeInterfaces = []
    for interface in netifaces.interfaces():
        ips = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in ips:
            for ip in ips[netifaces.AF_INET]:
                activeInterfaces.append({'name': interface, 'ip': ip['addr']})

    return activeInterfaces


def expose():
    containers = get_containers()
    for index, container in enumerate(containers):
        print('{} ) {}'.format(index, container.name))

    container = containers[int(input('Which machine do you want to expose? '))]
    exposed_port = input('Which port do you want to expose? ')

    os.system('iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT\
 --to-destination {}:80'.format(container.get_ips()[0]))

if __name__ == '__main__':
    expose()
