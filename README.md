# momo-api-django

A small django app for using the MOMO api to effect collections and reimbursements

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

- [] Create a model that resembles the data needed to create a collection resource in the Momo API
- [] Create a trigger that is called on every creation of a new instance of the MomoRequest model
- [] Create a function to make a request to the collections resource endpoint of the MOMO API preferrably with a url setting in the settings file
- [] Create a back ground task that keeps checking the status of the collections resource that would have been created in the MOMO API (how do you identify the resource?)
- [] Create a function/method/task that updates the status of the MomoRequest instance once
