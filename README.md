# Spezifikationsservice
_Proof-of-Concept_ Implementierung der _Spezifikationsservice_ -Komponente der _Privacy Proxy_ Architektur.

Es handelt sich um ...

## Nutzung

Im folgenden werden mögliche Wege aufgezeigt, um den Ausführungsservice zu testen:

a) lokale Ausführung

b) Ausführung als Cloud-Service

### Lokale Ausführung
Es wird die Nutzng einer vituellen Umgebung [(_virtualenv_)](https://www.dpunkt.de/common/leseproben//12951/2_Ihre%20Entwicklungsumgebung.pdf#page=15) empfohlen.

    >> pip install -r requirements.txt

    >> python PolSpecServ.py

Hinweis: Verzeichnis mit folgender Struktur:

    |-- config
    |   |-- myPolicies.txt
    |   :   ...
    |   `-- utilizerGraph.json
    |-- static
    |   |-- css
    |   |   |-- bootstrap-select.css
    |   |   |-- bootstrap-treeview.css
    |   |   |-- bootstrap.css
    |   |   `-- custom.css
    |   |-- fonts
    |   |   |-- glyphicons-halflings-regular.eot
    |   |   |-- glyphicons-halflings-regular.svg
    |   |   |-- glyphicons-halflings-regular.ttf
    |   |   |-- glyphicons-halflings-regular.woff
    |   |   `-- glyphicons-halflings-regular.woff2
    |   `-- js
    |       |-- bootstrap-select.js
    |       |-- bootstrap-treeview.js
    |       |-- bootstrap.js
    |       `-- jquery.js
    |-- templates
    |   |-- create.html
        :   ...
    |   `-- verify.html
    |-- requirements.txt
    |-- PolSpecServ.py
    |-- README.md
    |-- YaPPL_schema.json    
    `-- yappl.py
