# unbound-statistics-publisher

[![Python unit tests](https://github.com/qaldak/unbound-statistics-publisher/actions/workflows/python-tests.yml/badge.svg)](https://github.com/qaldak/unbound-statistics-publisher/actions/workflows/python-tests.yml)

## Description

Collects metrics from an Unbound Docker container and sends them to a receiver using MQTT (via Eclipse Mosquitto Docker
container).

## Getting started

### Execute

#### Command line

`python3 -m src.main <IP Address Receiver> [--no-reset] [--debug]`

optional parameter:

* "--no-reset" ("-nr") avoid to reset unbound statistics
* "--debug" set loglevel to DEBUG

#### Cronjob

`05 0 * * * cd <PATH> ; python3 -m src.main <IP Address> [--no-reset] [--debug]`

### Requirements

* Python 3.8 or higher
* Python modules, see [requirements.txt](requirements.txt)

### Links

#### Pyhton libraries

* [python-on-whales](https://github.com/gabrieldemarmiesse/python-on-whales)

#### Tools

* [eclipse mosquito](https://mosquitto.org/)
* [unbound](https://nlnetlabs.nl/projects/unbound/about/)

#### Docker images

there are much more Docker images for the same purpose. These here I used for this project:<br>

* [eclipse mosquito](https://hub.docker.com/_/eclipse-mosquitto) by the Eclipse Foundation
* [Unbound DNS Server Docker Image](https://hub.docker.com/r/mvance/unbound) by Matthew Vance

## Contribute

Contributions are welcome!

## Licence

Unless otherwise specified, all code is released under the MIT License (MIT).<br>
for used or linked components the respective license terms apply.
