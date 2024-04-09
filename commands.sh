#!/bin/bash

install_initial() {
    python -m venv venv
    source ./venv/Scripts/activate
    pip install django
    while true; do
        echo "Enter additional packages to install (separated by space), or press Enter to skip:"
        read packages
        if [ "$packages" ]; then
            pip install $packages
            pip freeze > requirements.txt
        else
            break
        fi
    done
    while true; do
        echo "Enter admin name:"
        read admin
        django-admin startproject $admin . && break
        echo "Failed to create project. Please try again."
    done
    while true; do
        echo "Enter app name (or 'quit' to stop):"
        read app
        if [ "$app" = "quit" ]; then
            break
        elif [ "$app" ]; then
            python manage.py startapp $app
            if [ -f "$app/fixtures/initial_data.json" ]; then
                python manage.py loaddata "$app/fixtures/initial_data.json"
            fi
        fi
    done
}

upgrede_pip() {
    source ./venv/Scripts/activate
    pip install -r requirements.txt
    echo "Pip has been upgraded."
}

install_pip() {
    source ./venv/Scripts/activate
    echo "Enter the name of the library to install:"
    read library
    pip install $library
    pip freeze > requirements.txt
    echo "$library has been installed."
}

remove_venv() {
    deactivate
    rm -rf venv
}

activate_venv() {
    source ./venv/Scripts/activate
}

add_admin() {
    source ./venv/Scripts/activate
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
}

migrate() {
    source ./venv/Scripts/activate
    python manage.py makemigrations
    python manage.py migrate
}

run() {
    trap 'kill $(jobs -p)' EXIT
    source ./venv/Scripts/activate
    python manage.py runserver 
    wait
}

mock_data() {
    source ./venv/Scripts/activate    
    echo "Enter app name (or 'all' to load all apps):"
    read app_name
    if [ "$app_name" = "all" ]; then
        for app in */; do
            if [ "$app" = "config/" ]; then
                echo "Skipping config app..."
                continue
            fi
            if [ -f "$app/fixtures/initial_data.json" ]; then
                python manage.py flush --no-input --database=default
                python manage.py loaddata "$app/fixtures/initial_data.json"
                echo "Loaded mock data for $app"
            else
                echo "No mock data found for $app"
            fi
        done
    else
        if [ "$app_name" = "config" ]; then
            echo "Cannot load mock data for config app"
            return
        fi
        if [ -f "$app_name/fixtures/initial_data.json" ]; then
            python manage.py flush --no-input --database=default
            python manage.py loaddata "$app_name/fixtures/initial_data.json"
            echo "Loaded mock data for $app_name"
        else
            echo "No mock data found for $app_name"
        fi
    fi
}
create_static() {
    mkdir media
    mkdir static
    mkdir templates
}

collectstatic () {
    source ./venv/Scripts/activate
    python manage.py collectstatic
}

reinstall() {
    python -m venv venv
    source ./venv/Scripts/activate
    pip install -r requirements.txt
}

echo "Enter command (install, activate, migrate, run, create, static, reinstall, remove, add_admin, mock_data, install_pip, upgrede_pip):"
read command
case $command in
    "install") install_initial ;;
    "migrate") migrate ;;
    "run") run ;;
    "mock_data") mock_data ;;
    "static") create_static ;;
    "reinstall") reinstall ;;
    "remove") remove_venv ;;
    "activate") activate_venv ;;
    "add_admin") add_admin ;;
    "collectstatic") collectstatic ;;
    "install_pip") install_pip ;;
    "upgrede_pip") upgrede_pip ;;
    *) echo "Unknown command" ;;
esac