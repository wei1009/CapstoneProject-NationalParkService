# National Park Service App

#### Try the App Here  <span> [https://national-park-search-service.herokuapp.com/](https://national-park-search-service.herokuapp.com/) </span>



## About the App
What is the best way to find the national park you want to visit? This is a search web app for national parks in the United States. This web app presents information of national park to users. Information includes national park introduction, activities and locations

## Features

1. Users can search for national parks by states, city and park name, users can also select a national park from the drop-down menu.
2. The page provides users with park information and a map.
3. Add ability to register, login and logout.
4. When user sign up, user can add the national park to favorites page.


## User Flow
<div style="text-align:center">
<img src="/images/userflow.jpg" width="90%"></img>
</div>

## Database Schema
<div style="text-align:center">
<img src="/images/schema.JPG" width="70%" ></img>
</div>

## APIs
National Park Service API: [https://developer.nps.gov/api/v1/parks](https://developer.nps.gov/api/v1/parks)  
Google Map API: [https://www.google.com/maps/embed/v1/place](https://www.google.com/maps/embed/v1/place)

## Tech Stack
Html, Css, Bootstrap,JavaScript, Python, Git, Visual Studio Code
<a href="https://www.w3.org/TR/html5/" title="HTML5"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" alt="HTML5" width="21px" height="21px"></a> &nbsp;<a href="https://www.w3.org/TR/CSS/" title="CSS3"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" alt="CSS3" width="21px" height="21px"></a> &nbsp;<a href="https://getbootstrap.com/" title="Bootstrap"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" alt="Bootstrap" width="21px" height="21px"></a> &nbsp; <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" title="JavaScript"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JavaScript" width="21px" height="21px"></a> &nbsp;<a href="https://www.python.org/" title="Python"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="21px" height="21px"> &nbsp;<a href="https://code.visualstudio.com/" title="Visual Studio Code"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" alt="Visual Studio Code" width="21px" height="21px"></a>

## How to find and run tests

To run a file containing unittests, you can run the command

```
FLASK_ENV=production python -m unittest test.py
```
