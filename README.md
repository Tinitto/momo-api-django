# momo-api-django

A small django app for using the MOMO api to effect collections and reimbursements

## Dependencies

- [Redis 5.0.5](https://redis.io)
- [Python ^3.5](https://www.python.org)
- [Celery 4.3](www.celeryproject.org)

## Scenario

```text
  With reference the The MTN MOMO API bellow;
  https://momodeveloper.mtn.com/api-documentation
  https://momodeveloper.mtn.com/products
  2.(a): Write a simple application in Python / Django that uses the MOMO API to effect   Collections and Disbursements to and from valid customer accounts
    i   - Create a database model class called MomoRequest to store the requests
    ii  - Automatically trigger a collection request whenever a new MomoRequest object is created
    - Collection: This operation is used to request a payment from a consumer (Payer). The payer will be asked to authorize the payment. The transaction will be executed once the payer has authorized the payment.
   iii - Periodically poll the status of any pending payments (Using an asynchronous task queue) and update the MomoRequest with the request status
  NB:
    - GUI code is not required, the application should just run from the terminal / shell
    - You can exclude boilerplate code that is not related to the assignment.
    - You don't need to have a functional MoMo Account as part of this assignment.
```

## Todos

- [x] Create a model that resembles the data needed to create a collection resource in the Momo API
- [x] Create a trigger that is called on every creation of a new instance of the MomoRequest model
- [x] Create a function to make a request to the collections resource endpoint of the MOMO API preferrably with a url setting in the settings file
- [x] Create a back ground task that keeps checking the status of the collections resource that would have been created in the MOMO API (how do you identify the resource?)
- [x] Create a function/method/task that updates the status of the MomoRequest instance once

## How to test (code snippets shown are for ubuntu 16.04)

- Ensure all the dependencies are installed and the redis-server is running.

  ```bash
  /usr/local/bin/redis-server --daemonize yes
  ```

- Clone the repo

  ```bash
  git clone https://github.com/Tinitto/momo-api-django.git
  ```

- Enter the `momo-api-django` directory and create a virtual environment and activate it

  ```bash
  cd momo-api-django && virtualenv -p /usr/bin/python3 env && source env/bin/activate
  ```

- Install the python dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Run the tests

  ```bash
  python manage.py runserver
  ```

## How to run locally

- Ensure all the dependencies are installed and the redis-server is running.

  ```bash
  /usr/local/bin/redis-server --daemonize yes
  ```

- Clone the repo

  ```bash
  git clone https://github.com/Tinitto/momo-api-django.git
  ```

- Enter the `momo-api-django` directory and create a virtual environment and activate it

  ```bash
  cd momo-api-django && virtualenv -p /usr/bin/python3 env && source env/bin/activate
  ```

- Install the python dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Open a separate terminal with the same folder active

  ```bash
  gnome-terminal
  ```

- In the new terminal (let's call it __Celery Worker terminal__), activate the virtual enviroment and then start the celery worker

  ```bash
  source env/bin/activate && celery -A momo_main_app worker -l info
  ```

- Open another terminal with the same folder active again

  ```bash
  gnome-terminal
  ```

- In the new terminal (let's call it __Celery Beat terminal__), activate the virtual enviroment and then start the celery beat

  ```bash
  source env/bin/activate && celery -A momo_main_app beat -l info
  ```

- Back to your very first terminal (the one which is not running anything to do with celery), open your django shell

  ```bash
  python manage.py shell
  ```

- An example to create a new MomoRequest of amount 500 euros for phonenumber '46733123450' in the shell is:

  ```python
  from momo_requests.models import MomoRequest
  
  new_momo_request = MomoRequest.objects.create(amount=500, currency='EUR', payer_party_id='46733123450')
  ```

- If you check the __Celery Worker terminal__, you should see a new entry with words along the lines of

  ```bash
  ...Received task: momo_requests.tasks.request_for_payment...
  ```

- If you check the __Celery Beat terminal__, you should see new entries every minute with words along the lines of

  ```bash
  ...Scheduler: Sending due task update-status-of-pending-every-minute (momo_requests.tasks.update_status_for_all_pending_payments)
  ```

  Corresponding to these new entries on __Celery Beat terminal__, you will be able to see more entries added successively on the __Celery Worker terminal__ with words along the lines of

    ```bash
    ...Received task: momo_requests.tasks.update_status_for_all_pending_payments...
    ```
