# unbound-metrics

## Description

Collects metrics from an Unbound Docker container and sends them to a receiver using another Docker container (e.g. via
Eclipse Mosquitto to an MQTT message broker).

## Getting started

### Execute

#### Command line

`python3 src/main.py "<IP Address Receiver>" [--debug]`

optional parameter "--debug" set loglevel to "DEBUG"

#### Cronjob

`05 0 * * * <PATH>/src/main.py "<IP Address Receiver>"`

### Dependencies

see [requirements.txt](src/requirements)

### Links

#### Pyhton libraries

* [python-on-whales](https://github.com/gabrieldemarmiesse/python-on-whales)

#### Tools

* [eclipse mosquito](https://mosquitto.org/)
* [unbound](https://nlnetlabs.nl/projects/unbound/about/)

#### Docker images

there are much more Docker images for the same purpose. These here I used for this project:<br>

* [eclipse mosquito](https://hub.docker.com/_/eclipse-mosquitto) by the Eclipse Foundation
* [Unbound DNS Server Deocker Image](https://hub.docker.com/r/mvance/unbound) by Matthew Vance

## Contribute

Contributions are welcome!

## Licence

Unless otherwise specified, all code is released under the MIT License (MIT).<br>
for used or linked components the respective license terms apply.