#!/bin/bash

service=${1}
[[ -z "${service}" ]] && echo "Usage: $0 <service name>" && exit 1

# Don't spam the honcho output. Only display the first time through
show_text=0
while [ true ]; do

  if brew services list | grep "${service}" | grep -i "start" | grep -v grep >/dev/null 2>&1; then
    [[ ${show_text} -eq 0 ]] && echo "brew services list for ${service} is running."
    pid_of=$(launchctl list | grep "homebrew.mxcl.${service}" | grep -v grep | awk '{ print $1 }')
    if [[ -n "${pid_of}" ]] && ps ${pid_of} >/dev/null 2>&1; then
      [[ ${show_text} -eq 0 ]] && echo "ps shows ${service} is running. PID: ${pid_of}"
    else
      # Display the exit text otherwise honcho just stops quietly
      echo "ps shows ${service} as not running."
      break
    fi
  else
    echo "brew services list for ${service} is not running."
    break
  fi

  sleep 5

  # avoid spamming output starting the second time through
  show_text=$((show_text + 1))

done
