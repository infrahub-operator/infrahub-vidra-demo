from flask import Flask, render_template, request
import sys
import os
from typing import Union

# Add the path for the Python script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from python_scripts.createobjects import createwebserver, createvirtuellmaschine

app = Flask(__name__)


# Route for the input page
@app.route("/", methods=["GET", "POST"]) # type: ignore
def index() -> str:
    """This function displays the form and processes it when submitted.

    It receives user input, calls the Python script, and returns the result.
    """
    if request.method == "POST":
        deployment_type = request.form.get("deployment_type")
        name = request.form.get("name").replace(" ", "_")
        description = request.form.get("description").replace(" ", "_")
        namespace = request.form.get("namespace").replace(" ", "_")
        url = request.form.get("url")
        image = request.form.get("image")

        # Example: Call a Python script with the input values
        result = run_python_script(
            deployment_type,  
            name,  
            description,  
            namespace, 
            url,
            image,
        )

        return render_template("index.html", result=result)  # type: ignore

    return render_template("index.html", result=None)  # type: ignore


# Function that executes the Python script
def run_python_script(
    deployment_type: str,
    name: str,
    description: str,
    namespace: str,
    url: Union[str, None],
    image: Union[str, None],
) -> str:
    """This function calls the Python script `createwebserver` and processes the return value.

    Depending on the result, a confirmation or an error message is returned.
    """
    try:
        # Call the createwebserver function and forward the results
        match deployment_type:
            case "Webserver":
                result = createwebserver(name, description, namespace, image)  # type: ignore
            case "VM":
                result = createvirtuellmaschine(name, description, namespace, url)  # type: ignore
            case _:
                result = -1  # Return Error

        # Check the return value and respond accordingly
        return f"""
            Your {deployment_type} is requested!\n
            As soon as the Network Administrator has accepted your request, your {deployment_type} will be available under:\n
            {result}\n
            Thank you!
        """

    except Exception as e:
        # Error handling: Log the error and return a message
        print(f"Error while processing the request: {e}")
        return """
            An unexpected error occurred. Please try again later.
            If the problem persists, please contact your network administrator.
            {response}
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
