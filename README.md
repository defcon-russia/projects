# projects
Initial files for building 'projects' page on your github.io hosted web site

Installation steps:

  1 - Fork this repo to your account
  
  2 - Clone repo to you local machine, i.e. to /home/user/projects/ directory
  
  3 - Run catalog.py with 2 arguments (full path to local copy of 'projects' folder 
  and full URL where 'projects' will be deployed), i.e.
  
      python catalog.py -p /home/user/projects/ -u http://mywebsite.github.io/projects
      
  4 - Script will create all the files in /home/user/projects/ directory
  
  5 - Edit static pages (about, ideas, submit)
  
  6 - If you want to add new project - just add it projects.json file and run script
  
  7 - Push changes to your github repo
