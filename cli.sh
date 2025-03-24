#!/bin/bash

tput smcup # Switch to alternate screen
export GUM_FILTER_PLACEHOLDER_BACKGROUND="212"

export WorkspaceId=0
export ProjectId=0
export RunId=0

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
    main exit
  fi

  workspace_id=$(echo "$workspaces" | jq -r --arg workspace "$workspace" '.[] | select(.name == $workspace) | .id')
  export WorkspaceId=workspace_id
  choose_project
}

####################################################################

function get_projects() {
  projects=$(curl -s -X POST "http://localhost:8000/project/$WorkspaceId" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN")
  echo "$projects"
}

function choose_project() {
  projects=$(get_projects)

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
    choose_workspace
    exit
  fi

  project_id=$(echo "$projects" | jq -r --arg project "$project" '.[] | select(.name == $project) | .id')
  printf $project_id
  choose_run $project_id
}

####################################################################

function get_run() {
  runs=$(curl -s -X POST "http://localhost:8000/run/$ProjectId" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN")
  echo "$runs"
}

function choose_run() {
  runs=$(get_run)
  if [ "$(echo "$runs" | jq 'length')" -eq 0 ]; then
    run_list="Back"
  else
    run_list=$(
      echo "$runs" | jq -r ".[].name"
      echo "Back"
    )              