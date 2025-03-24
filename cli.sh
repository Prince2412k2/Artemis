#!/bin/bash

tput smcup # Switch to alternate screen
export GUM_FILTER_PLACEHOLDER_BACKGROUND="212"

####################################################################

function get_all_users() {
  all_users=$(curl -sLX 'GET' 'http://127.0.0.1:8000/user/get_all' -H 'accept: application/json' | jq -r '.[].name')
  all_users=$(
    echo "$all_users"
    echo "Back"
  ) # Ensure "Back" is a separate line

  choice=$(gum filter <<<"$all_users")
  if [ "$choice" = "Back" ]; then
    return # Return to main menu instead of calling exit incorrectly
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
    exit 1
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
  echo "$workspaces"
}

function choose_workspace() {
  workspaces=$(get_workspaces)

  if [ -z "$workspaces" ] || [ "$workspaces" = "null" ]; then
    echo "No workspaces found."
    return
  fi

  ws_list=$(
    echo "$workspaces" | jq -r ".[].name"
    echo "Back"
  )
  workspace=$(gum filter --placeholder "Workspaces" <<<"$ws_list")

  if [ "$workspace" = "Back" ]; then
    main
    exit
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

  if [ -z "$projects" ] || [ "$projects" = "null" ]; then
    echo "No projects found."
    return
  fi

  ps_list=$(
    echo "$projects" | jq -r ".[].name"
    echo "Back"
  )
  project=$(gum filter --placeholder "Projects" <<<"$ps_list")

  if [ "$project" = "Back" ]; then
    choose_workspace
    return
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

  if [ -z "$runs" ] || [ "$runs" = "null" ]; then
    echo "No runs found."
    return
  fi

  run_list=$(
    echo "$runs" | jq -r ".[].name"
    echo "Back"
  )
  run=$(gum filter --placeholder "Runs" <<<"$run_list")

  if [ "$run" = "Back" ]; then
    choose_project "$1"
    return
  fi

  run_id=$(echo "$runs" | jq -r --arg run "$run" '.[] | select(.name == $run) | .project_id')
  echo "$run_id"
}

function main() {
  # Main Menu
  choice=$(gum filter --placeholder "Menu" <<<"Register"$'\n'"Login"$'\n'"ALL_USERS"$'\n'"EXIT")

  case "$choice" in
  "ALL_USERS") get_all_users ;;
  "Login")
    login
    workspace_id=$(choose_workspace)
    project_id=$(choose_project "$workspace_id")
    run_id=$(choose_run "$project_id")
    ;;
  "EXIT") exit 0 ;;
  esac
}

main
