# Tiny shelter archive
 
The end goal of this project is to provide a repository for DIY campervan builds.

## Installation

There is a requirements.txt in the project directory. With these apps installed, my project is run via the manage.runserver command. 

## Usage

When the app is loaded, a user has the option to browse the database for shelter builds. He/she can see vehicles of a specified type or furniture posts of a specified type or predominant build technique. The user is advised of steps required to contribute his/her build to the database. To do so requires registering for the site, adding a vehicle, and building the vehicle with furniture. Up to 7 annotated photos can be added to the main vehicle post and each child furniture element. Every registered user has a profile. Users can message one another through a simple in-app messaging system. 

# Distinctiveness
This project shares some elements from previous projects but has distinct form and function. Its database structure is more complex. Its function is entirely unique. The implementation is far more advanced and less hacky than previous than those given as my solution to previous problem assignments. I challenged myself to as much code RE-use as possible - largely in thanks to class based views inheriting from Django's generic views.
 
# Complexity

The site functions well and all its cross connections - which are numerous -  work. The forms are really nice. For example, 7 images and annotations for each furniture - but via a formset only so many forms as the user requests are displayed. The editing functions work for every user submission - including there profile view. There are password reset and email authentications functions. The layout is sufficient and workable as a beta version. It is mobile responsive but needs development to become professional grade. I intend to do a complete revamp of the formatting following this project submission. I will be getting rid of all bootstrap and delving deep into purely manual css layout control. 


# Files: an overview of file contents

The root directory is called 'final'. In addition to django preset files, it has some base templates and static and media files. Of special note is the javascript file containing the The main app - 'website' - is in the directory of that name. Here we find mainly the usual suspects. I do define a Layout class in custom_layout_object.py and have a couple custom django template filters in a template tags directory. The views map to namespaced templates directory with descriptive names; for example, garage.html is the tempalte for the GarageView and list_furniture.html lists furniture for all the search functions. 
