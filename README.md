# KreisAnordnungsTool
Fusion 360 App - runde Kreisstrukturen mit gleichem Lochabstand automatisch erstellen

KreisAnordnungsTool ist ein benutzerfreundliches Fusion-360-Add-In zum schnellen Erzeugen von Kreis-Anordnungen in einer aktiven Skizze. Damit lassen sich in wenigen Schritten perfekte Sieb-Strukturen anlegen oder 3D-gedruckte Lüftungsgitter gestalten. Einfach einen Startpunkt auswählen, Durchmesser und Kopienanzahl bestimmen – den Rest erledigt das Add-In. Ideal für alle, die funktionale, gleichmäßig verteilte Kreisanordnungen in ihren CAD-Modellen benötigen.

# Highlights:
- freiwählbarer Startpunkt für die Struktur
- Individueller Durchmesser der "Löcher"
- Individueller Abstand der "Löcher"
- Anzahl der Durchgänge (Anzahl der Kreis-Ringe)
- Spare Zeit und erstelle automatisch die "Löcher-Struktur"

![KreisAnordnungsTool Dialog](images/Kreis-Anordnungs-Tool-Dialog.png)

![KreisAnordnungsTool erstellte Skizze](images/Sieb-Skizze.png)

![KreisAnordnungsTool erstelltes Sieb](images/Sieb-Beispiel.png)

# Installation:
## Add-In herunterladen
Lade zunächst das komplette Add-In-Paket als Release-Archiv von GitHub herunter.

## Zip-Datei entpacken
Entpacke das Archiv in einen beliebigen Ordner auf deinem Computer (z. B. „Dokumente“).

## Fusion 360 starten & Add-In-Verwaltung aufrufen
- Öffne Fusion 360.
- Wähle in der oberen Menüleiste „TOOLS“ → „Add-Ins“ (bzw. „Scripts and Add-Ins“).

## Add-In importieren
- Klicke im neu geöffneten Fenster auf den Reiter „Add-Ins“ (nicht „Scripts“).
- Klicke unten rechts auf „+“ (oder „Add“).
- Navigiere in den Ordner, den du zuvor entpackt hast, und wähle dort den Add-In-Ordner (mit manifest.json).
- Bestätige die Auswahl.

## Add-In aktivieren
- Markiere nun in der Liste dein neues Add-In.
- Klicke auf „Run“ oder „Activate“, damit Fusion 360 dein Add-In lädt.
- Optional kannst du das Häkchen bei „Run on Startup“ setzen, damit sich das Add-In beim nächsten Fusion-Start automatisch lädt.

## Einsatz des Add-Ins prüfen
- Wechsle in Fusion 360 zurück ins Design-Fenster.
- Im Erstellen-Panel unter Konstruktion erscheint nun im Menu (ganz unten) der neue Eintrag "VersatzebenenTool"
- Klick darauf, um das Add-In auszuführen

![Tool im Menü](images/VersatzebenenToolMenu.png)

## Tipp:
- Wenn du das Add-In aktualisierst (z. B. neue Version), wiederhole Schritt 4 bzw. kopiere die aktualisierten Dateien in denselben Ordner.
- Unter Windows liegt das Standard-Add-Ins-Verzeichnis meist in
C:\\Users\\<Benutzername>\\AppData\\Roaming\\Autodesk\\Fusion 360\\API\\AddIns.
- Unter macOS findest du es unter
~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns.

Viel Erfolg bei der Installation!
