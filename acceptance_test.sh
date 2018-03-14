#!/bin/bash

if curl localhost:8000 | grep -q 'Welcome to your new Wagtail site!'; then
  echo "Endpoint test passed!"
  exit 0
else
  echo "Endpoint test failed!"
  exit 1
fi
