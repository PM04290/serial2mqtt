## serial2mqtt

Passerelle lisaison serie (HA input) vers un serveur MQTT

## Configuration

| Param          | Description              |
|----------------|--------------------------|
| uart           | /dev/ttyUSB0, /dev/ttyACM1, etc. |
| baud           | 57600                            |
| mqtt_server    | core-mosquitto ou IP             |
| mqtt_user      | username pour login              |
| mqtt_pass      | password pour login              |
| mqtt_topic     | topic abonné                     |
| debug          | pour afficher dans le log        |


## Fonctionnement

L'entrée est au format JSON

Le contenu de topic est une clé connue de configuration.yaml

Exemple pour un switch

{"topic":"mqtt_topic/monswitch/state", "payload": "ON"}

Exemple pour un sensor

{"topic":"mqtt_topic/moncapteur/value", "payload": "12.6"}
