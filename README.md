# movie-picker
In my home we have some trouble deciding on a movie to watch. My husband has seemingly endless numbers of movies on his list to check out, which makes choosing one all the more difficult. We had your old standard paper movie jar for a while (where you randomly draw a movie), but it doesn't help us filter based on our mood, how much time we have, or the audience, and is cumbersome to change the options. This application therefore upgrades a standard paper movie jar with modernized flexibility including more sophisticated filtering. 

# How it works 
As the user, you can have as many "jars" as you would like and can edit those jars with various movies. When the '+' button is clicked within a created jar, you'll be prompted for a title, and the application searches TMDB for both TV shows and movies and displays them to you, so you can pick your desired option. The app will then automatically gather the required data of the selected movie(s)/show(s). The user is prompted to select a "vibe" for their selection -- basically, determine whether the movie is challenging emotionally and/or mentally to watch. This is a major source of challenge in deciding a movie for us that genre doesn't quite determine for us, but it is easy to ignore this feature if you wish. If you would like other custom filter options, please let me know, as this would be of interest to me for future development. 

The 'Your Jars' page displays your movies in an attractive card format organized by jar, and hovering over those movies displays additional information on the back of the card. The user can edit their entries and include a custom rating if they've already watched the movie. Watched movies are stored in a "watched" movie jar as well, for interest sake. 

The movie picker tool at the top of the page prompts the user for a run time, jar to choose from, vibe, and genre for the movie. It chooses the highest rated as a "top pick" suggestion, but displays all the others that meet the search criteria as well.  


# How to use
This app can be previewed here: ______________________.
However, this is not suitable for use of the application, as there is no user sign in and your data will be erased after a single use. It is simply here to demonstrate the concept. The reason for this is one of scope and acknowledgment of my current limitations -- I need to learn more before I am comfortable hosting your data in this way. This is the next step for this project though, so please stay tuned if this is something of interest to you. 

Currently, for my own personal use, I am running this application on my home computer. If you would like to do the same, here are some instructions for how you could go about doing so from the code provided in this repository. 

## For Windows: 
1. Download this repository and note where on your computer you download the folder. 

2. Ensure python is installed on your computer. If you need to install, go here: https://www.python.org/downloads/ and make sure you click on the "add python to path" checkbox so python and needed packages are available to the program. You also need to download pip: https://www.liquidweb.com/kb/install-pip-windows/ 

3. Open windows powershell and navigate to the directory you downloaded this repository: ```cd C:/path/to/directory```

4. Download the requirements by running: ```pip install -r requirements.txt```

5. You need to define two environment variables to run this program. 

      1. SECRET_KEY : You can randomly generate a secret key here: https://randomkeygen.com/
      
      2. TMDB_API_KEY : is obtained from TMDB for using their API service. Go here to get one: https://developers.themoviedb.org/3/getting-started/introduction  
      
    To add these environment variables to your PATH, type in Powershell:
   
   ``` $env:SECRET_KEY="YOUR_SECRET_KEY" ``` 
   
   ``` $env:TMDB_API_KEY="YOUR_TMDB_API_KEY" ```
   
6. The program can then be launched by typing: 
  ``` waitress-serve --host 127.0.0.1 main:app ```
  
  If you have chrome installed, the website should automatically launch. Otherwise, copy/paste "http://127.0.0.1:8080" into your browser's address bar to see the application. Your data will be saved locally on your machine in the instance/movies.db location inside the folder you downloaded this repository. 

## Desktop shortcut: 
To make a desktop shortcut to conveniently launch the application: 

1. Set permission to run .ps1 scripts on your machine. Note this will allow scripts you personally write to run, but maintain protection against scripts that haven't been properly authenticated.
```Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned```

2. Make a script called "run.ps1" and put it in the program directory. Inside, add the following code, customized with your environment variables and path to this folder. 
``` $env:SECRET_KEY="YOUR_SECRET_KEY"; $env:TMDB_API_KEY="YOUR_TMDB_API_KEY"; cd C:/path/to/movie-picker; waitress-serve --host 127.0.0.1 main:app ```

3. On your desktop, right click "create shortcut" and in the Target window type the following, changing the path to your own for the run.ps1 script. 
```C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -noexit  -ExecutionPolicy Bypass C:/path/to/run.ps1```. Hit save. 

4.  Double clicking on the created shortcut should launch the program as before. If you would like to start the application on a different browser, edit line 162 of main.py as needed. 
