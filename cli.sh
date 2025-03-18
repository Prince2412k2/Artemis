#!/bin/bash

curl -X 'POST' \
  'http://localhost:8000/workspace/get' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCMzUiLCJleHAiOjE3NDIyOTU2Njd9.aQCmn0jmarKJrflNGLAfx3HDPo-uN6j8QJ7KcSF1l_A' \
  -d ''
