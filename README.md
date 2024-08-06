# Car Rental API

This is a Flask-based API for managing car rentals. The API allows users to log in, manage cars, and rent cars. It includes endpoints for user authentication, car management, and car rentals.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Testing](#testing)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/balumanobiram/workindia
2. **Install the dependencies:**

   ```sh
   pip install Flask psycopg2

## Configuration

1. **Database Configuration**

   In the file dbprop.json change the properties of the database

   ```sh
   {
    'host': 'localhost',
    'database': 'database_name',
    'user': 'username',
    'password': 'password'
   }

2.**Create the following tables**

   ```sh
   CREATE TABLE public.car_data
   (
       category text,
       model text,
       number_plate text,
       current_city text,
       rent_per_hr integer,
       rent_history jsonb
   )

   CREATE TABLE public.userlogin_details
   (
       username text,
       password text,
       email text,
       user_id integer,
   )



   
