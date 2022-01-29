# A pricing test mocker that mocks a successful test

from threading import Event
print('Pricing test beginning')
Event().wait(2)
print('Initialisation complete')
Event().wait(5)
print('Primary tests complete')
Event().wait(8)
print('Secondary tests complete')
Event().wait(5)
print('SUCCESS')