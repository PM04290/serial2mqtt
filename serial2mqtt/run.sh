#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

UART="$(jq --raw-output '.uart' $CONFIG_PATH)" \
BAUD="$(jq --raw-output '.baud' $CONFIG_PATH)" \
MQTT_SERVER="$(jq --raw-output '.mqtt_server' $CONFIG_PATH)" \
MQTT_USER="$(jq --raw-output '.mqtt_user' $CONFIG_PATH)" \
MQTT_PASS="$(jq --raw-output '.mqtt_pass' $CONFIG_PATH)" \
MQTT_TOPIC="$(jq --raw-output '.mqtt_topic' $CONFIG_PATH)" \
DEBUG="$(jq --raw-output '.debug' $CONFIG_PATH)" \

python3 /main.py "$UART" "$BAUD" "$MQTT_SERVER" "$MQTT_USER" "$MQTT_PASS" "$MQTT_TOPIC" "$DEBUG"