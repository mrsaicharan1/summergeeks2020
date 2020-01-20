# Innovaccer SDE Challenge
> An Entry Management software

## Docker Image

https://hub.docker.com/repository/docker/mrsaicharan1/checkin-sys

## Installation

OS X & Linux:

```sh
git clone https://github.com/mrsaicharan1/summergeeks2020
```

## Approach
To track the Visitors of the office, we are storing the details of the person in the `Visitor` table where we can find name(`string`), phone(`string`), email(`string`) and timestamps(`DateTime`). This has been implemented using the ORM tool SQLAlchemy along with Flask.
To build the forms for visitors and Hosts, `Flask-WTForms` is being used as a form builder. 

Before a visitor enters the building, they need to fill out the `Visitor CheckIn` form. They fill in their name, email, phone and select a host from the list of hosts who are currently available(Hosts who do not have a checkout time). After clicking on submit, this data is `POST`ed onto the server-side route `checkin/visitor` which contains the logic to store the details in the `Visitors` table using the ORM. A Twilio API client object is created and the SMS is sent with the entered form details. Leveraging the Sendgrid API, a `Mail` object is created and the necessary details are sent to the host with the current timestamp using Python's `datetime` module. The user receives a unique code via an SMS by which they can check out at the end. This aids in evading someone to else to check out on their name.
As this function is used everywhere, this has been shifted to the helpers module to comply with `DRY principles`
Similarly, a host check-in form has also been implemented with similar logic.

A visitor/host can check out by entering their checkout code. The checkout code is verified and the checkout time is updated to the current time by querying the SQLAlchemy table using this checkout code in the `/checkout` route. As soon as this is done, the visit details are sent using the `send_mail` helper function present in `helpers` module.

## Server Side Routes
+ `/`
    - This route automatically redirects to `checkin/visitor`

+ `/checkin/visitor`
    - The default home route for our web app which includes the logic for storing the visitor's details and sending an SMS and email alerts about the new visitor.
+ `/checkin/host`
    - Contains the logic for storing the host's details and checking them in. 

+ `/checkout`
     - A visitor/host can checkout using their checkout code here. The app verifies the code and updates the checkout time. If a host has checked out, they're removed from the list of available hosts at check-in. If a visitor checks out, the checkout time is updated.

## Front End WTForms
The base forms are constructed right into `forms.py`. The valid data types and additional form handling rules are present here.
The form templates are present in `templates/forms` where one can find the front-end Jinja code for form handling. Other templates such as error pages, base layouts are also present in the `templates` directory.

# SQLAlchemy Table Design/ Database
Our database comprises of two tables namely:
- Visitor
- Host

The `Visitor` table was created with the `SQLAlchemy` Engine with the following fields:
+ name : `String`
+ phone : `String`
+ email : `String`
+ check_in : `DateTime`
+ check_out : `DateTime`
+ host_id : `Integer`, `Foreign Key`

The `Host` table was created with the `SQLAlchemy` Engine with the following fields:
+ name : `String`
+ phone : `String`
+ email : `String`
+ check_in : `DateTime`
+ check_out : `DateTime`
+ visitors: `relationship`

Here, we establish a *many-to-one* relationship as one host may have many visitors. Therefore, we declare a visitors relationship in the `Host` table and the foreign key as `host_id` in `Visitor` table. SQLAlchemy automatically creates a link between both the tables once a relationship is specified in one of them with the foreign key in the other. We don't need to rewrite/replicate the code in the other table.


## Tech Stack 

+ Flask - Backend
+ Jinja - Templating Engine
+ HTML, CSS - Front End
+ SQLite - Database(SQLAlchemy ORM)

## Development setup

To set up the project, we need to install all dependencies using `pip` dependency manager
If you don't have pip installed,

```
sudo apt-get install python3-pip
```

Set up a virtual environment and activate it to avoid dependency issues.

```
virtualenv venv
.venv/bin/activate
```

Install the required dependencies using the following command
```
pip3 install -r requirements.txt
```

Before starting the server, for mailing and SMS to work, you need Twilio and Sendgrid API credentials.
These need to be stored as environment variables after creating the .env file as follows
```
cp .env.example .env
```

Open up the `.env` file and fill in the API keys for Twilio(**auth_token** and **account_sid**)& Sendgrid

After this, whip up the server using the following command

```
python3 app.py
```

and navigate to http://localhost:5000

## Release History

* 1.0.0
    * Initial Version


## Contributing

1. Fork it (<https://github.com/mrsaicharan1/summergeeks2020>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


