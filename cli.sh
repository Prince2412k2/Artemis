#!/bin/bash

tput smcup # Switch to alternate screen
export GUM_FILTER_PLACEHOLDER_BACKGROUND="212"


####################################################################

function get_all_users() {
  all_users=$(curl -sLX 'GET' 'http://127.0.0.1:8000/user/get_all' -H 'accept: application/json' | jq -r '.[].name')
  all_users=$(
    echo "$all_users"
    echo "Back"
  )

  choice=$(gum filter <<<"$all_users")
  if [ "$choice" = "Back" ]; then
    main exit # Go back to main menu
  fi
}

####################################################################

function login() {
  username=$(gum input --prompt "Username : " --placeholder "Enter your username")
  password=$(gum input --password --prompt "Password : " --placeholder "Enter your password")

  token=$(curl -s -X POST 'http://127.0.0.1:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "username=$username&password=$password" | jq -r '.access_token')

  if [ -z "$token" ] || [ "$token" = "null" ]; then
    echo "Login failed. No token received."
    main exit # Avoid script exit
  fi
  export TOKEN="$token"
  echo "Login successful!"
}

####################################################################

function get_workspaces() {
  workspaces=$(curl -s -X POST 'http://localhost:8000/workspace/my' \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN")

  if [ -z "$workspaces" ] || [ "$workspaces" = "null" ]; then
    echo "No workspaces found."
    main exit
  fi
  echo "$workspaces"
}

function choose_workspace() {
  workspaces=$(get_workspaces)
  if [ -z "$workspaces" ]; then return; fi

  ws_list=$(
    echo "$workspaces" | jq -r ".[].name"
    echo "Back"
  )
  workspace=$(gum filter --placeholder "Workspaces" <<<"$ws_list")

  if [ "$workspace" = "Back" ]; then
    main exit # Go back to previous step
  fi

  workspace_id=$(echo "$workspaces" | jq -r --arg workspace "$workspace" '.[] | select(.name == $workspace) | .id')
  echo "$workspace_id"
}

####################################################################

function get_projects() {
  projects=$(curl -s -X POST "http://localhost:8000/project/$1" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN")
  echo "$projects"
}

function choose_project() {
  projects=$(get_projects "$1")

  if [ "$(echo "$projects" | jq 'length')" -eq 0 ]; then
    project="Back"
  else
    ps_list=$(
      echo "$projects" | jq -r ".[].name"
      echo "Back"
    )
  fi

  project=$(gum filter --placeholder "Projects" <<<"$ps_list")

  if [ "$project" = "Back" ]; then
    choose_workspace # Go back to workspace selection
    exit
  fi

  project_id=$(echo "$projects" | jq -r --arg project "$project" '.[] | select(.name == $project) | .workspace_id')
  echo "$project_id"
}

####################################################################

function get_run() {
  runs=$(curl -s -X POST "http://localhost:8000/run/$1" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN")
  echo "$runs"
}

function choose_run() {
  runs=$(get_run "$1")
  if [ "$(echo "$runs" | jq 'length')" -eq 0 ]; then
    run="Back"
  else
    run_list=$(
      echo "$runs" | jq -r ".[].name"
      echo "Back"
    )
  fi

  run=$(gum filter --placeholder "Runs" <<<"$run_list")

  if [ "$run" = "Back" ]; then
    choose_project "$1"
    exit
  fi

  run_id=$(echo "$runs" | jq -r --arg run "$run" '.[] | select(.name == $run) | .project_id')
  echo "$run_id"
}

function main() {
  while true; do
    choice=$(gum filter --placeholder "Menu" <<<"Register"$'\n'"Login"$'\n'"ALL_USERS"$'\n'"EXIT")

    case "$choice" in
    "ALL_USERS") get_all_users ;;
    "Login")
      login
      if [ -n "$TOKEN" ]; then
        workspace_id=$(choose_workspace)
        if [ -n "$workspace_id" ]; then
          project_id=$(choose_project "$workspace_id")
          if [ -n "$project_id" ]; then
            run_id=$(choose_run "$project_id")
          fi
        fi
      fi
      ;;
    "EXIT") exit 0 ;;
    esac
  done
}

main
