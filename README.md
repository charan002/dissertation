Mongo DB - 
  
  Use MongoDB Compass (GUI). Link: "https://www.mongodb.com/try/download/compass".
  
  Run the following comands to install MongoDB Community edition
  
    brew tap mongodb/brew 
    brew install mongodb-community                     #To install MongoDB.
    brew services start mongodb-community              #To start the MongoDB services.

  By default, MongoDB uses "mongodb://localhost:27017/" port. Provide 'Project Name' field as "projectdb".
  On the GUI app, create a new connection and connect and save.

Tailwind CSS - 
  
  First install Node.js with the following command.
  
    brew install node                                  #To install Node.js.
    node -v                                            #To verify the installation and version of Node.js.
    npm -v                                             #To verify the installation and version of npm (Node Package Manager).
    npm install                                        #To install dependencies. 

    npm audit fix                                      #To fix any vulnerabilities. Once run, vulnerabilities should be fixed.

  Now install Tailwind CSS
    
    npm install -D tailwindcss                         #To install Tailwind CSS.
    npx tailwindcss init                               #To create Tailwind configuration file.
    npx tailwindcss -i ./static/styles/style.css -o ./static/styles/output.css --watch    #Keeps Tailwind running and: 1. Watches HTML/JS/template files 2. Auto rebuilds CSS when you save

To run the application, use the following command.

    flask run --debug
