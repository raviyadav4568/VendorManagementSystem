
# Vendor Management System

Vendor Management System lets you create vendor profiles, track purchase orders and to create performance metrics.

## Tech Stack

**Server:** Python, Django, MySql

## Installation

(Note: Project requires Python 3.11 as the supported python version.)

To install it on your development environment, create a folder name Vendor management system and under the same directory using cli, install django 

```bash
  pipenv install django
```

If you don't have pipenv already, download it using pip
```bash
  pip install pipenv
```

Download the source code and move it to the vendor management system folder, once that is done start the virtual environment 

```bash
  pipenv shell
```

Once under the virtual environment, start the localhost server 
```bash
  python manage.py runserver
```
Try hitting the below endpoint to check the Installation
```bash
  http://127.0.0.1:8000
```

Once the server is up and running, we need to migrate the database table to mysql server, for which we need to create the database first, use the below command in mysql server to create the database

```bash
  CREATE DATABASE vendormanagementsystem;
```

We need to install mysql client for communication between mysql and python. Type the following command in shell to install mysqlclient

```bash
  pipenv install mysqlclient
```

Before we can do the migrations we need to change the db settings in project settings file

```bash
  goto vendormanagementsystem/vendormanager/settings.py

  change following settings, make sure to set the user and password with valid credentials

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'vendormanagementsystem',
        'HOST':'localhost',
        'USER':'root', # mysql username
        'PASSWORD':'1234' # mysql username password
    }
}
```

Now we need to migrate the tables from django to mysql server, for which we need to make the migrations using below command

```bash
  python manage.py makemigrations
```

And then migrate

```bash
  python manage.py migrate
```

Check the database for the migrated tables. Use the provided dummy.sql file to import dummy data for testing. Run the dummy.sql file in mysql server using the below command
```bash
  source 'file location';
```

To use the api we need to create a user and an authenticaion token.
To create a user using any api testing tool hit a post request on the below url with username, email and password in the request body (Note: all credentials in string)
```bash
  http://127.0.0.1:8000/create_user
```
Copy the returned token. This token is required for authentication.
```bash
  "Token: efc965dc3b5f01a7788c802ca6c1b9a5aff54f3f"
```

Now the api's can be used to test the functionalities.



## API Reference

### Vendor Management Endpoints

#### To create user and for generating token

```http
  POST /api/create_user
```

| Body | Type     | Description                | Response|
| :-------- | :------- | :------------------------- | :---   |
| `username, email, password` | `string` | Following data has to be provided in body of the request | Authentication Token |

#### To list all Vendors

```http
  GET /api/profilemanager/vendors
```

| Parameter | Type     | Description                       | Response |
| :-------- | :------- | :-------------------------------- |:-- |
| None      | None | None | List all the Vendors | List of all the vendors |


#### To create a new vendor

```http
  POST /api/profilemanager/vendors
```
| Body | Type     | Description                       | Response |
| :-------- | :------- | :-------------------------------- | :-- |
| vendor_code, name, contact_details, address | String | To create a new vendor, post request is send to the above endpoint with the mentioned parameter in the body of the request  | Details of the new vendor created |


#### To get details of a specfic vendor

```http
  GET /api/profilemanager/vendors/<vendor_code>
```

| Parameter | Type     | Description                       | Response |
| :-------- | :------- | :-------------------------------- | :- |
| vendor_code      | Int | Vendor Code is provided in the url to get the vendor details | Details of that specific Vendor |


#### To update a Vendor Details

```http
  PUT /api/profilemanager/vendors/<vendor_code>
  PATCH /api/profilemanager/vendors/<vendor_code>
```
The above endpoint supports PUT, PATCH request to support all kinds of update to the Vendor Details 

| Body |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| Parameters to update | Variable type| Parameters with updated value must be sent in the body of the request  | Updated vendor details          |

#### To get Vendor Performance details

```http
  GET /api/profilemanager/vendors/<vendor_code>/performance
```

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| Vendor Code | Int| Vendor Code is provided in the above endpoint to performance metrics of that specific vendor  | Performance metrics of a Vendor        |


#### To delete any Vendor

```http
  DELETE /api/profilemanager/vendors/<vendor_code>
```

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| Vendor Code | Int| Vendor Code is provided in the above endpoint with delete request to delete a specfic vendor          | Http 204 No Content response           |

### Purchase Order Management Endpoints

#### To List all Purchase Order

```http
  GET /api/purchase_order_tracking/purchase_orders
```

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| None | None|  To get all the vendors hit the above endpoint with a get request        | List of Purchase Orders |


#### To Create a new Purchase Order

```http
  POST /api/purchase_order_tracking/purchase_orders
```

| Body |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| `po_number,vendor,delivery_date,items,quantity,status,issue_date` | - |  To create a new purchase order hit the above endpoint with mentioned parameters in the body of the request| Details of the Purchase Order Created|
    

#### To get details of a Purchase Order

```http
  GET /api/purchase_order_tracking/purchase_orders/<po_number>
```

| parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| `po_number` | Int |  To get more details of a purchase order hit the above endpoint with po_number in the url| Details of that Purchase Order |


#### To Update details of a Purchase Order

```http
  PUT /api/purchase_order_tracking/purchase_orders/<po_number>
  PATCH /api/purchase_order_tracking/purchase_orders/<po_number>
```
The above endpoint supports PUT, PATCH request to support all kinds of update to the Purchase Order

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| `po_number` | Int |  To update a purchase order hit the above endpoint with details to update in the body of the request| Details of the updated Purchase Order |


#### To Acknowledge a Purchase Order

```http
  GET /api/purchase_order_tracking/purchase_orders/<po_number>/acknowledge
  POST /api/purchase_order_tracking/purchase_orders/<po_number>/acknowledge
```
Purchase order can be acknowledged with GET as well as POST method. If the endpoint is hit with a get request, current datetime is set as acknowledgement date. Post method is used to give user defined datetime to acknowledgement date by passing datetime in the body of the request

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| `po_number` | Int |  To acknowledge a purchase order hit the above endpoint with the po_number of the purchase order to acknowledge| Updated Acknowledgement Date |


#### To DELETE a Purchase Order

```http
  DELETE /api/purchase_order_tracking/purchase_orders/<po_number>
```

| Parameter |  Type       |   Description         |  Response         |
| :------     | :------ |  :------   | :------   |
| `po_number` | Int |  Delete a purchase order by hitting the above endpoint with a valid po_number| Http 204 No Content response |

### Test Suite
Test suite is present in the source code of the project for testing the project and its functionalities.
















