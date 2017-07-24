#!/bin/bash

import png:- | zbarimg png:- | grep ^QR-Code: | sed -e 's/^QR-Code:\(.*\)$/\1/g' | ./uri2ss.py
