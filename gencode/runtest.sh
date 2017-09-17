#!/bin/bash

./main.py
cd test/vstest/
echo
echo ---begin build---
./build.sh
echo ---end build---
echo
echo
echo ---begin test---
./vstest/vstest
echo ---end test---
