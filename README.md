# Fixed Gear Community Map

A web application for fixed gear enthusiasts to connect and share their passion for cycling.

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Technical Requirements](#technical-requirements)
* [Installation](#installation)
* [Usage](#usage)

## Introduction

The Fixed Gear Community Map is a web application designed to connect fixed gear cyclists from around the world. The
application allows users to create profiles, share photos of their bikes, and connect with other riders in their area.

## Features

* User profiles with bike photos and descriptions
* Map view to connect with other riders in your area
* Photo gallery to showcase your bike
* User authentication and authorization using Django's built-in auth system
* RESTful API for interacting with the application data

## Technical Requirements

* Python 3.11
* Django 5.1.2
* Django REST framework 3.15.2
* Django Countries 7.6.1
* Font Awesome Free 6.6.0
* Pillow 11.0.0
* Requests 2.32.3
* SQLite 3.38.5

## Installation

1. Clone the repository: `git clone https://github.com/matousidc/fixed_gear_community_map.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a new SQLite database: `python manage.py migrate`
4. Run the development server: `python manage.py runserver`

## Usage

1. Navigate to `http://localhost:8000/map/` to access the application
2. Create a new user account by clicking on the "Register" button
3. Fill out your user profile and add photos of your bike
4. Use the map view to connect with other riders in your area

