#!/bin/bash -e

if which google-chrome &>/dev/null && which certutil &>/dev/null;
then
    if [ ! -d ${HOME}/.pki/nssdb ];
    then
        mkdir -p ${HOME}/.pki/nssdb
        certutil -d sql:${HOME}/.pki/nssdb -N --empty-password
    fi
    # RedHat based distros
    if [ -d /etc/pki/ca-trust/source/anchors ];
    then
        for cert in /etc/pki/ca-trust/source/anchors/*;
        do
            certutil -d sql:${HOME}/.pki/nssdb/ -A -t C -n $(echo ${cert} | rev | cut -f 2- -d '.' | cut -f 1 -d '/' | rev) -i ${cert}
        done
    fi
    # Debian based distros
    # TODO
    #   We need to slim this down to just the certs we are adding somehow.
    #   This directory contains all the certs for the system.
    #if [ -d /usr/local/share/ca-certificates ];
    #then
    #    for cert in /usr/local/share/ca-certificates/*;
    #    do
    #        certutil -d sql:${HOME}/.pki/nssdb/ -A -t C -n $(echo ${cert} | rev | cut -f 2- -d '.' | cut -f 1 -d '/' | rev ) -i ${cert}
    #    done
    #fi
    # FreeIPA cert
    if [ -f /etc/ipa/ipa.crt ];
    then
        certutil -d sql:${HOME}/.pki/nssdb/ -A -t C -n /etc/ipa/ipa.crt -i ${cert}
    fi
fi
