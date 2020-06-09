#!/bin/bash

if [[ -z "${1}" ]]; then
  commands="join help mute list who stop update private start test resend invite random_movie"
elif [[ ${1} == "-h" || ${1} == "--help" ]]; then
  echo "Usage:"
  echo "1. Test a single command: ${0} #command"
  echo " <prompt>$ ${0} random_movie"
  echo "2. Test a single command with arguments: args="argument1 argument2" ${0} #command"
  echo " <prompt>$ args=off ${0} private"
  echo "3. Test all commands: ${0}"
  echo " <prompt>$ ${0}"
  echo "4. Test all commands with arguments: args="argument1 argument2" ${0}"
  echo " <prompt>$ args=foobar ${0}"
  echo "   ** this is mostly to check that the command is counting arguments correctly, not really useful otherwise"
  echo
  exit
else
  commands=${1}
fi

if [[ -z "${TWILIO_MYNUM}" ]]; then
  echo "Set the env var TWILIO_MYNUM to your mobile, using the format +15555555555"
  exit 1
fi

for c in ${commands}; do
  curl -X POST http://localhost:5300/txt/async -d "From=${TWILIO_MYNUM}" -d "Body=#${c} ${args}"
done
