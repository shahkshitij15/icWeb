# icWeb
An automated virtual assistant for people with visual impairements

## Problem we solve
People with visual impairements are restricted in tasks that are common-place for other people, web browsing is one of them. There are some solutions on the market, but all of these rely on screen readers and heavily use a keyboard interace for user commands, for these people lerning the keyboard shortcuts is a real challenge, we aim to create an entirely voice based interface to access the most popular websites on the internet. Users will be able to issue voice commands to control the browser, the contents of which will be read out to them. We have added convenient features like - Wikipedia articles can be queried using a state of the art machine learning model for question answering, and they can also be summarised.

DEMO : https://www.youtube.com/watch?v=ak5i_hcOex0

Documentation:- https://devfolio.co/submissions/icweb



dir google


    code for scraping and voice automating google.com


dir wiki


    code for querying the wiki api for text and summaries of their articles.


    Code also to load and run the bert model for question answering


dir mail


    code to voice automate gmail.com


stt.py, tts.py


    util files for speech to text and text to speech functions

chromedriver


    the chrome browser driver used by selenium to automate web browsing
    
    
main.py


    main file which calls all the other functions

Running instructions: 


1. The user will open the terminal using voice assistant in his laptop


2. The user will then navigate to the site of file and run the program by using the shortcuts set initially i.e. python main.py 


3. Once the program is run the user has to simply input his/her search query and enjoy the browsing experience
