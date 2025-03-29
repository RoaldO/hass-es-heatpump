#!/usr/bin/env bash

export PROJECT_ROOT='/home/roald/Projects/hass-es-heatpump'
export DOMAIN='DOMAIN'
export USERNAME='homeassistant'
export PASSWORD='i545g17vx6++'
export SHARE='smb://homeassistant.local/config/custom_components/es/'
export AUTH="${DOMAIN}\\${USERNAME}:${PASSWORD}"

for file in ${PROJECT_ROOT}/custom_components/es/*
do
  echo "transferring ${file}"
  curl --upload-file ${file} -u $AUTH ${SHARE}
done
