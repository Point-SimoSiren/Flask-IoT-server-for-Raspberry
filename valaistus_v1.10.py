# Sovellus on tehty Pythonin flask ja GPIO kirjastoilla Rapberry pi:tä silmälläpitäen.
# Sisältää palvelimen, joka palauttaa html sivun, jonka painikkeilla annetaan http pyynnöt
# Tämän ohjelman reitteihin valojen käyttämiseksi GPIO pinnien kautta.

import RPi.GPIO as GPIO

# asennettava ensin flask npm työkalulla, sitten voidaan kutsua sen kolmea liitännäiskirjastoa
from flask import Flask, render_template, request

app = Flask(__name__)

# Otetaan käyttöön broadcomin numerointisysteemi
GPIO.setmode(GPIO.BCM)

# pinnien talletuspaikan luonti
pins = {
    23: {"name": "GPIO 23", "state": GPIO.LOW},
    24: {"name": "GPIO 24", "state": GPIO.LOW},
}

# Output määritys ja alustus sammutetuksi
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# palvelimen reitti: aloitustilanne
@app.route("/")
def main():

    # silmukka pinnien tilan lukemiseen yhteyden alussa
    for pin in pins:
        pins[pin]["state"] = GPIO.input(pin)

    # edellä luodut talletuspaikat sisällytetään templateData muuttujaan
    templateData = {"pins": pins}

    # Palautetaan käyttöliittymään html sivu ja templateData
    return render_template("main.html", **templateData)


# Api reitti pinni nro / toimenpide on/off
@app.route("/<changePin>/<action>")
def action(changePin, action):

    # URL stringistä otetaan pin kokonaisluvuksi
    changePin = int(changePin)

    # Käsiteltävän pinnin laitetunniste-nimi selvitetään
    deviceName = pins[changePin]["name"]

    # Päällekytkentätilanteessa ajettava
    if action == "on":
        # Pinni päälleasentoon
        GPIO.output(changePin, GPIO.HIGH)
        # Statusviestin muodostus
        message = "Valo " + deviceName + " päällä."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Valo " + deviceName + " sammutettu."

    # Luetaan taas kaikkien pinnien tila ja talletetaan alussa luotuun talletuspaikkaan
    for pin in pins:
        pins[pin]["state"] = GPIO.input(pin)

    templateData = {"pins": pins}
    # Palautetaan tilatieto käyttöliittymään
    return render_template("main.html", **templateData)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

