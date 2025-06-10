from flask import Flask, render_template, request
import sys
import os
from typing import Union

# Ergänze den Pfad für das Python-Skript
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from python_scripts.createobjects import createwebserver, createvirtuellmaschine

app = Flask(__name__)


# Route für die Eingabeseite
@app.route("/", methods=["GET", "POST"]) # type: ignore
def index() -> str:
    """Diese Funktion zeigt das Formular an und verarbeitet es, wenn es abgesendet wird.

    Sie nimmt Benutzereingaben entgegen, ruft das Python-Skript auf und gibt das Ergebnis zurück.
    """
    if request.method == "POST":
        deployment_type = request.form.get("deployment_type")
        name = request.form.get("name").replace(" ", "_")
        description = request.form.get("description").replace(" ", "_")
        namespace = request.form.get("namespace").replace(" ", "_")
        url = request.form.get("url")
        image = request.form.get("image")

        # Beispiel: Aufruf eines Python-Skripts mit den Eingabewerten
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


# Funktion, die das Python-Skript ausführt
def run_python_script(
    deployment_type: str,
    name: str,
    description: str,
    namespace: str,
    url: Union[str, None],
    image: Union[str, None],
) -> str:
    """Diese Funktion ruft das Python-Skript `createwebserver` auf und verarbeitet die Rückgabe.

    Je nach Ergebnis wird eine Bestätigung oder eine Fehlermeldung zurückgegeben.
    """
    try:
        # Aufruf der createwebserver Funktion und Weiterleitung der Ergebnisse
        match deployment_type:
            case "Webserver":
                result = createwebserver(name, description, namespace, image)  # type: ignore
            case "VM":
                result = createvirtuellmaschine(name, description, namespace, url)  # type: ignore
            case _:
                result = -1  # Return Error

        # Überprüfung des Rückgabewertes und entsprechende Antwort
        return f"""
            Your {deployment_type} is requested!\n
            As soon as the Network Administrator has accepeted your request, youre {deployment_type} will be available under:\n
            {result}\n
            Thank you!
        """

    except Exception as e:
        # Fehlerbehandlung: Logge den Fehler und gib eine Nachricht zurück
        print(f"Error while processing the request: {e}")
        return """
            An unexpected error occurred. Please try again later.
            If the problem persists, please contact your network administrator.
            {response}
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
