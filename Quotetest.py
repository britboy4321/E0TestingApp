# A pricing test mocker that mocks a FAILED test

from threading import Event
print('Quoting test beginning')
Event().wait(2)
print('Initialisation complete')
Event().wait(9)
print('Primary tests complete')
Event().wait(13)
print('No response recieved')
Event().wait(5)
print('FAIL')