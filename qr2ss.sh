#!/bin/bash

import png:- | zbarimg png:- | sed -e 's/QR-Code:\(.*\)/\1/g' | ./uri2ss.py
