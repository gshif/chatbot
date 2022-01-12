Chatbot is an automated regression testing framework suitable for testing chatbot applications.
Chatbot is based on pytest open source framework and uses python for writing tests and supporting libraries.

Chatbot can be run as a `docker container` or from a local repository.

**Chatbot Framework**
---------------------

- **To display help**
  - By running the command from ROOT level (chatbot):
    1. `cp scripts/run_master.py . && chmod +x run_master.py`
    2. `./run_master.py -h`


- **Running Chatbot**
  - It accepts either a test file(s) or test lists.
    - Test files (start with **`test_`**) group related tests into test classes. One test file might have more than one test class.
  If a feature has multiple sub-features, then one test file would be named `test_task_1`, `test_task_2`, etc.
  Currently it has only one test file with one test class.
    - Inside the test file (sub-features) tests can be grouped based on sub-sub-features into
  corresponding test classes, e.g. `TestTaskSub1` class, `TestTaskSub2` class, etc. In order to pass a single test file
  use **`--tests <path to a test file>`**
    - If there is a need to run multiple test files at once, for example, having one test run to test `featureA`, 
  where testing of `featureA` is organized into multiple test files. All of the `tests lists` could be found under 
  `chatbot/tests_lists` directory. In order to pass a list of tests to be executed, 
  use **`--tests-lists <path to a test list file>`**
    - A log file will be created in the `result` directory named `chatbot.log`. it could be configured in `pytest.ini` file along with 
    file log level and log format values. In the future, log file will be created for each test file (TODO).

- **Writing tests**
  - TBD

- **How to run Litmus from a docker container locally**
  - To build a chatbot image locally, run `docket build -f Dockerfile -t <chatbot:tag> `
  
  **Running One Test**
    - >docker run --net host --rm -e URL=ws://localhost -e PORT=4444 \
       -e ONE_TEST=src/tests/test_websocket.py \
       -v </path to/>/chatbot/result:/Chatbot/result chatbot:<tag>     
  
  **Running Test List**
    - >docker run --net host --rm -e URL=ws://localhost -e PORT=4444 \
       -e TEST_LIST=tests_list/test_all.list \
       -v </path to/>/chatbot/result:/Chatbot/result chatbot:<tag>
    
- **How to run Chatbot from local repository**  
    - Prerequisites for running test(s) from local repo:
      - You need to be in `chabot` dir.
      - Copy `run_master.py` script from `chatbot/scripts` directory to `chatbot` directory.
      - Test(s) must be run from `chatbot` directory.
     
  **Running One Test** 
  
    - >./run_master.py --url ws://localhost --port 4444 \
       --tests src/tests/pods_resources/test_pods.py 
      
  **Running List Of Tests**
    - >./run_master.py --url ws://localhost --port 4444 \
       --tests-list tests_list/test_all.list

 
NOTE: 
- Not all the scenarios are covered by the tests in the test_websocket.py

  