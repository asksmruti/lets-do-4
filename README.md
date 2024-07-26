# lets-do-4
PoC for Survey Template



* Install Python Version - 3.10.14

    ```
    pyenv install 3.10.14
    pyenv virtualenv 3.10.14 dev
    pyenv local dev
    ```
* Install requirements.txt
    ```
    pip install -r requirements.txt
    ```

* Run the application
    `python run.py` 

    ```
    INFO:     Uvicorn running on http://127.0.0.1:4000 (Press CTRL+C to quit)
    INFO:     Started reloader process [59706] using WatchFiles
    INFO:     Started server process [59758]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```
* Check the Open API docs

```
Open following links on browser for interactive API documentation 

http://127.0.0.1:4000/docs

Open following link to know more about schemas
http://127.0.0.1:8000/redoc

```

* The survey template can also be updated with curl command. Here is one example -

```
curl -X PUT http://127.0.0.1:4000/update-section/Needs \
-H "Content-Type: application/json" \
-d '{
    "section": "Needs",
    "questions": [
        {
            "type": "multi-choice",
            "question": "What is the primary reason for your purchase?",
            "options": ["Replacement", "Upgrade", "Remodel", "Gift"]
        }
    ]
}'
```

* Run the unit tests (Both postive and negative)
    `pytest test_main.py`

    ```
    ======================================================================= short test summary info ========================================================================
    FAILED test_main.py::test_update_section - assert 500 == 200
    FAILED test_main.py::test_delete_question - assert 404 == 200
    FAILED test_main.py::test_add_question - assert 422 == 201
    FAILED test_main.py::test_update_question - assert 422 == 200
    ===================================================================== 4 failed, 6 passed in 0.93s ======================================================================
    ```
