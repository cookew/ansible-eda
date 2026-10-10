#!/bin/bash

set -e

# Search directories for NSS database
PKI_SEARCH_DIRS=(
  "${HOME}/.pki/nssdb"
  "${HOME}/.local/share/pki/nssdb"
)

# What directory to create if none of the search directories exist
PKI_MKDIR="${HOME}/.pki/nssdb"

if ! which google-chrome &>/dev/null || which certutil &>/dev/null
then
  # Exit because google-chrome or certutil is not detected
  exit
fi

for d in "${PKI_SEARCH_DIRS[@]}"
do
  if [ -d "${d}" ]
  then
    PKI_DIR_EXISTS=1
    break
  fi
done

if [ "${PKI_DIR_EXISTS}" -ne 1 ]
then
  mkdir -p "${PKI_MKDIR}"
  certutil -d sql:"${PKI_MKDIR}" -N --empty-password
fi

for d in "${PKI_SEARCH_DIRS[@]}"
do
  if [ -d "${d}" ]
  then
    # Get list of existing certificates in the NSS database
    NSS_EXISTING_CERTS=$(certutil -d sql:"${d}" -L)

    # Import certificates from RHEL based ca directories
    if [ -d /etc/pki/ca-trust/source/anchors ]
    then
      for cert in /etc/pki/ca-trust/source/anchors/*;
      do
        # Skip importing the certificate if it already exists in the NSS database
        if echo "${NSS_EXISTING_CERTS}" | grep -q "$(basename "${cert}")"
        then
          continue
        fi
        cert_basename=$(basename "${cert}")
        certutil -d sql:"${d}" -A -t C -n "${cert_basename}" -i "${cert}"
      done
    fi
    # Import certificates from Debian based ca directories
    # TODO
    #   We need to slim this down to just the certs we are adding somehow.
    #   This directory contains all the certs for the system.
    # if [ -d /usr/local/share/ca-certificates ]
    # then
    #  for cert in /usr/local/share/ca-certificates/*;
    #  do
    #    # Skip importing the certificate if it already exists in the NSS database
    #    if echo "${NSS_EXISTING_CERTS}" | grep -q "$(basename "${cert}")"
    #    then
    #      continue
    #    fi
    #    cert_basename=$(basename "${cert}")
    #    certutil -d sql:"${d}" -A -t C -n "${cert_basename}" -i "${cert}"
    #  done
    # fi
  fi
done

# FreeIPA cert
if [ -f /etc/ipa/ipa.crt ]
then
  certutil -d sql:"${HOME}/.pki/nssdb/" -A -t C -n ipa.crt -i /etc/ipa/ipa.crt
fi
