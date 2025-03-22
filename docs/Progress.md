# Progress 

## Setup and organizing
1. Initialize the `uv` with `uv init` command
2. Install the flask by `uv pip install flask` command
3. Created the `app` directory
4. Created the `app/__init__.py` for adding the backend code inside the `app` directory
5. Created the `app/routes.py` for adding the view functions
6. Exported the `FLASK_APP=main.py` to the environment
7. Tested the execution of the flask app by `flask run` command
8. Installed the python dot env for saving the environment variables, helpful for using environment variable and to install use `uv pip install python-dotenv` 
9. Created the `.flaskenv` for storing the environmental variables for this application
10. Created a directory named `app/templates`
11. Inside the `app/templates/` directory, created the `index.html` 
12. By using the `render_template()` function the `html` code is rendered in the webpage.
13. Can able to add `title` arg in the `render_template()` as it is optional and `html` contains the `{% if title %}` and `{% else %}` and `{% endif %}` for conditional rendering.
14. Created a base template in `base.html` that acts as `layout.jsx` in react based applications.
15. Updated the `app/templates/index.html` with the block named `content`
16. To make the active reload of the flask app, run with `flask run --debug` command
17. Created `app/static` folder for storing the `css` files
18. Splitted the `base.html` into multiple files like `main.html`, `navbar.html` and `footer.html`

## Backend logic implementation
1. Added the file upload logic to the `routes.py` and updated the `main.html` for previewing the file
2. Added the cards in the main html file for uploading the image, previewing the image and getting the result image.
3. Downloaded the SAM 2 model from the sam2 github repository
4. Inference code is added to get the final result
5. For better user experience overlay image is added in the `preview_image()` function