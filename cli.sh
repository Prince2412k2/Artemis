#!/bin/bash

tput smcup # Switch to alternate screen

function get_all_users() {
  all_users=$(curl -sLX 'GET' 'http://127.0.0.1:8000/user/get_all' -H 'accept: application/json' | jq -r '.[].name')
  all_users+="\nExit" # Append 'Exit' option
  echo "$(gum filter <<<"$all_users")"
}

function login() {
  username=$(gum input --prompt "Username : " --placeholder "Enter your username")
  password=$(gum input --password --prompt "Password : " --placeholder "Enter your password")
  token=$(curl -s -X POST 'http://127.0.0.1:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "username=$username&password=$password" | jq -r '.access_token')
  echo "$token"
}

function get_token() {
  token=$(login)

  if [ -z "$token" ]; then
    echo "Login failed. No token received."
    exit 1
  fi
  echo $token
}

function get_workspaces() {
  workspaces=$(curl -s -X POST 'http://localhost:8000/workspace/my' \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $1")
  echo "$workspaces"
}

function get_projects() {
  projects=$(curl -s -X POST "http://localhost:8000/project/$1" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $2")
  echo "$projects"
}

function choose_project() {
  projects=$(get_projects $1 $2)

  if [ -z "$projects" ] || [ "$projects" = "null" ]; then
    echo "No projects found."
    exit 1
  fi
  ps_list=$(echo "$projects" | jq -r ".[].name")
  ps_list+=" Back"
  project=$(gum filter $ps_list)
  if [ "$project" = "Back" ]; then
    choose_workspace $2
    exit 0
  fi
  project_id=$(echo "$projects" | jq -r --arg project "$project" '.[] | select(.name == $project) | .workspace_id')
  echo $project_id
}

function choose_workspace() {
  workspaces=$(get_workspaces $1)

  if [ -z "$workspaces" ] || [ "$workspaces" = "null" ]; then
    echo "No workspaces found."
    exit 1
  fi
  ws_list=$(echo "$workspaces" | jq -r ".[].name")
  ws_list+=" Back"
  workspace=$(gum filter $ws_list)
  if [ "$workspace" = "Back" ]; then
    $(main)
  fi
  workspace_id=$(echo "$workspaces" | jq -r --arg workspace "$workspace" '.[] | select(.name == $workspace) | .id')
  echo $workspace_id
}

function main() {
  # Main Menu
  choice=$(gum filter "Register" "Login" "ALL_USERS" "EXIT")

  if [ "$choice" = "ALL_USERS" ]; then
    get_all_users
  elif [ "$choice" = "Login" ]; then
    token=$(get_token)
    workspace_id=$(choose_workspace "$token")
    project_id=$(choose_project $workspace_id "$token")
  fi
}
main
