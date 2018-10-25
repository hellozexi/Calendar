# calendar

## team members

* Jason Zhu, 467138
* Zexi Liu, 467319

## Additional Details

project URL:

<http://ec2-52-14-93-16.us-east-2.compute.amazonaws.com:8080/>
Welcome to your own calendar.
1. Double click on the day box to create a event of that day. Once you click, you will see the dialog below.   
2. Edit you event after click on the "edit" button right next to that event. When you click that, there will be a dialog under the calendar. By using that dialog, you can add tags or make some changes to your event.
3. Delete it by using "del" button.
4. Highlight your tags by clicking on the tags you created.
5. Delete your tags by clicking it. Look at the dialog below and you will find the delete button.
6. You can use the input field or "prev" and "next" button on the right top of the page to visit any month!
7. If you can't remember all the instructions, check the "help" button and you will find what you need.

## Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:8080 my_calendar:app --daemon
```

## Creative Portion

1. Users can tag an event with a tag and enable/disable those tags in the calendar view.
2. Users can unregister their account, which would automatically delete all events they create
3. All web api and server-side code are completely under unittest

## requirements.txt
1. all packages are listed in requirements.txt, you can create a python virtualenv and install all of them.
2. the python version should be 3.6

## python unittest
* you can run all unittests with command below, and remember the env requirement.
* Since there are a ORM framework as a abstract layer, in unittest we can use sqlite file database instead the product database.
```bash
python3 -m unittest discover -v
```
