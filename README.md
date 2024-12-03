Planung: - Optimierung der Kompression:
KI-Modelle (z. B. neuronale Netze) analysieren die Datei, um bessere Mustererkennung und Vorhersage zu ermöglichen als herkömmliche Kompressionsalgorithmen. Sie könnten spezifisch für den Datentyp trainiert werden (z. B. Spiele, Bilder, Videos).
Beispiel: Statt redundante Texturen direkt zu speichern, wird ein allgemeines Texturmuster generiert und nur die Abweichungen davon gespeichert.

    - Segmentierung:
        Das KI-Modell teilt die Datei in Segmente auf, die einzeln komprimiert und unabhängig übertragen werden können. Dies erlaubt eine parallele Übertragung

    - Prozedurale Rekonstruktion:
        Statt z. B. alle Texturen eines Spiels als Binärdaten zu speichern, könnten Algorithmen die Texturen dynamisch generieren (z. B. durch prozedurale Algorithmen wie Perlin Noise für Oberflächen).
        Das Regelwerk für diese prozeduralen Inhalte wird mit den Daten mitgeliefert. Der Empfänger führt es aus, um die Inhalte zu rekonstruieren.

    - Optimale Delta-Kompression innerhalb der Datei:
        Auch ohne vorherige Daten auf der Empfängerseite lässt sich innerhalb der Datei selbst Delta-Kompression nutzen:

        Wiederholende Blöcke erkennen: Viele Dateien, besonders Spiele, enthalten Redundanzen, z. B. mehrfach genutzte Texturen, wiederholte Codebausteine oder ähnliche Datenstrukturen. Diese könnten als Referenz gespeichert werden, anstatt sie mehrfach zu übertragen.
        Interne Struktur analysieren: Ähnlich wie bei Deduplizierung in Dateisystemen können gleiche Datenblöcke erkannt und nur einmal übertragen werden.

    - Parallele Übertragung mit Fehlerkorrektur:
        Die Datei wird in kleinere unabhängige Blöcke aufgeteilt:

        Unabhängige Kompression: Jeder Block wird einzeln komprimiert (z. B. mit Zstandard oder Brotli).
        Paralleler Transfer: Diese Blöcke werden parallel übertragen, um die verfügbare Bandbreite optimal zu nutzen.
        Fehlerkorrektur: Moderne Fehlerkorrekturverfahren wie Reed-Solomon-Codes minimieren die Notwendigkeit, fehlende Daten erneut anzufordern.

    - Optimierung für Spiele und Programme:
        Bei Spielen / Programme gibt es oft typische Bestandteile, die optimiert übertragen werden können:
            Assets (Texturen, Modelle, Sounds):
                Prozedurale Generierung: Sofern möglich, Texturen und andere Daten prozedural generieren.
                Komprimierte Archive: Für Daten, die sich nicht prozedural generieren lassen, können bestehende Archive (z. B. ZIP-ähnlich) optimiert verwendet werden.

            Code und Skripte:
                Skripte und binärer Code können durch klassische Kompressionstechniken optimiert werden, da diese meist keinen großen Speicherbedarf haben.

            Vermeidung von Redundanzen:
                Viele Spiele nutzen dieselben Bibliotheken (z. B. Unity- oder Unreal-Assets). Solche Bibliotheken könnten global gespeichert und nur spezifische Daten des Spiels übertragen werden.


    - Verschlüsselung
        Files / Downloads / Archive etc. sollen Verschlüsselt werden können. Minimum die Aktuellen Verschlüsselungsarten.
        Mehrfachverschlüsselung und verschlüsselte Übertragung inklusive Key Basierte verschlüsselung, Segementierte Verschlüsselung (die einzelenen Segemente / Chunks).


    - Idee Transfer:
        Analyse durch den Sender:
            Das Spiel wird analysiert, in Segmente unterteilt und hochkomprimiert.
            Prozedural generierbare Inhalte werden definiert.
            Die Datei wird in unabhängige, optimal komprimierte Blöcke aufgeteilt.

        Übertragung zum Empfänger:
            Die Blöcke werden parallel übertragen.
            Fehlerkorrektur stellt sicher, dass alle Daten korrekt ankommen.

        Rekonstruktion auf der Empfängerseite:
            Der Empfänger dekomprimiert die Blöcke.
            Prozedurale Inhalte werden lokal generiert.
            Die Daten werden zusammengeführt, um die Originaldatei (das Spiel) zu rekonstruieren.

        Anforderung von Files:
            Der "Client" soll die möglichkeit haben Files via Link, Container oder ähnlichen Files aus dem Internet anzufordern.

        Filesharing:
            Der "Client" soll die möglichkeit bekommen Files wie ein Filesharing Programm anzubieten und zu verteilen.
            Benutzer sollen Files freigeben können und diese zum Download / Upload anbieten können.
            Der Benutzer soll alternativ zum Beispiel via API's Files zu "OneClick" Hoster hochladen können. (Verschlüsselt)

        Sicherheit:
            Der Transfer muss verschlüsselt sein. Ggf. neue Verschlüsselung entwerfen oder mehrere Verschlüsselungen kombinieren
            Über mehrere Verschlüsselte Kanäle Transferieren inkl. Tor.

- Erste Ziele des Projekts:

Universelles Pack- und Entpack-Tool:

- Unterstützt alle gängigen Formate (ZIP, RAR, 7ZIP) sowie experimentelle eigene Kompressionstechniken.
  Erweiterbar durch Plugins für weitere Kompressionsverfahren.

- Datentransfer:
  Dateien können in Blöcken übertragen und bei Fehlern rekonstruiert werden.
  Fehlerkorrektur-Mechanismen und parallele Übertragung.

- Langfristige Erweiterungen:
  KI-gestützte Kompression: Erkennung von Redundanzen und Mustern.
  File-Browser: Integriertes System für Archivverwaltung.
  Kommunikation: Chat und Dateianfragen zwischen Sender und Empfänger.
  Optimierung für Spiele: Unterstützung prozeduraler Inhalte und effiziente Asset-Kompression.

Aufbau:
smart_transfer/
├── main.py # Hauptsteuerung des Programms
├── compression_manager.py # Verwaltung der Plugins
├── compression_plugin_base.py # Basisklasse für alle Plugins
├── packer.py # Packen von Dateien/Ordnern
├── unpacker.py # Entpacken von Dateien
├── sender.py # Daten senden und komprimieren
├── receiver.py # Daten empfangen und rekonstruieren
├── plugins/ # Ordner für Plugins
│ ├── **init**.py # Markiert 'plugins' als Paket
│ ├── zstandard_plugin.py # Zstandard-Kompressionsplugin
│ ├── zip_plugin.py # ZIP-Kompressionsplugin (geplant)
│ ├── rar_plugin.py # RAR-Kompressionsplugin (geplant)
│ └── 7zip_plugin.py # 7ZIP-Kompressionsplugin (geplant)

Meilensteine

    Muss überarbeitet werden:
        Grundlegende Architektur.
        Modularität und Plugin-System.
        Zstandard-Kompressionsplugin.

    In Arbeit:
        Integration von ZIP-, RAR- und 7ZIP-Plugins.
        Verbesserte Benutzerinteraktion und Fortschrittsanzeige.

    Zukünftig:
        KI-gestützte Kompression.
        Prozedurale Rekonstruktion.
        Filebrowser und Chat.

Future Plan: Rust/Tauri oder C++

    Rust/Tauri:
        Ideal für moderne GUIs mit Webtechnologien.
        Hohe Sicherheit und Performance.
    C++:
        Perfekt für maximale Kontrolle und Geschwindigkeit.
        Einfache Integration nativer Bibliotheken wie 7-Zip.
