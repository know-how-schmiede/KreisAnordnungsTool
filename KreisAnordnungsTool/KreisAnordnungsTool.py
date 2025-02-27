import adsk.core, adsk.fusion, adsk.cam, traceback
import math

# Globale Liste für Event-Handler, damit Python-Objekte nicht
# vorzeitig vom Garbage Collector gelöscht werden.
handlers = []

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        cmdId = 'KreisAnordnungsTool'
        cmdName = 'Kreis-Anordnungs-Tool'
        cmdDescription = (
            'Erstellt einen Kreis am Startpunkt, ' 
            'legt eine lineare Anordnung in x-Richtung an '
            'und erzeugt für jeden Kreis (außer dem 1.) '
            'eine runde Anordnung um den Basiskreis.'
        )

        # Falls die CommandDefinition existiert, zuerst entfernen.
        existingCmdDef = ui.commandDefinitions.itemById(cmdId)
        if existingCmdDef:
            existingCmdDef.deleteMe()
        
        # Neue CommandDefinition mit Icon (resources/myicons/...)
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            cmdId,
            cmdName,
            cmdDescription,
            'resources/myicons/KreisAnordnungsTool'  # Basispfad der Icons
        )
        
        # Event-Handler registrieren
        onCommandCreated = CommandCreatedEventHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        
        # Befehl im "SketchCreatePanel" platzieren
        sketchPanel = ui.allToolbarPanels.itemById('SketchCreatePanel')
        cmdControl = sketchPanel.controls.addCommand(cmdDef)
        cmdControl.isPromoted = True
        cmdControl.isPromotedByDefault = True
        
    except:
        if ui:
            ui.messageBox('Fehler in run:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        cmdId = 'KreisAnordnungsTool'
        
        # Befehl aus dem Skizzen-Panel entfernen
        sketchPanel = ui.allToolbarPanels.itemById('SketchCreatePanel')
        cmdControl = sketchPanel.controls.itemById(cmdId)
        if cmdControl:
            cmdControl.deleteMe()
        
        # CommandDefinition entfernen
        cmdDef = ui.commandDefinitions.itemById(cmdId)
        if cmdDef:
            cmdDef.deleteMe()
            
    except:
        if ui:
            ui.messageBox('Fehler in stop:\n{}'.format(traceback.format_exc()))


class CommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    """Dialog-Setup, wenn der Befehl gestartet wird."""
    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        cmd = args.command
        inputs = cmd.commandInputs
        
        # 1) Auswahl eines Skizzenpunkts (Startpunkt)
        selInput = inputs.addSelectionInput(
            'startPoint',
            'Startpunkt wählen',
            'Wähle einen Skizzenpunkt.'
        )
        selInput.setSelectionLimits(1, 1)
        selInput.addSelectionFilter('SketchPoints')
        
        # 2) Kreisdurchmesser
        inputs.addValueInput(
            'circleDiameter',
            'Kreis-Durchmesser',
            'mm',
            adsk.core.ValueInput.createByReal(10.0)  # Standard 10 mm
        )
        
        # 3) Anzahl Kopien (lineare Anordnung)
        inputs.addIntegerSpinnerCommandInput(
            'numCopies',
            'Anzahl Kopien (x-Richtung)',
            0,    # Minimum
            100,  # Maximum
            1,    # Schritt
            2     # Standardwert
        )
        
        # 4) Abstand (mm) zwischen den Kreisen
        inputs.addValueInput(
            'circleSpacing',
            'Abstand pro Kopie',
            'mm',
            adsk.core.ValueInput.createByReal(10.0)  # Standard 10 mm
        )
        
        # Handler fürs Ausführen
        onExecute = CommandExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    """Wird ausgeführt, wenn der Benutzer auf 'OK' klickt."""
    def notify(self, args: adsk.core.CommandEventArgs):
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        cmd = args.command
        inputs = cmd.commandInputs
        
        selInput     = inputs.itemById('startPoint')
        diaInput     = inputs.itemById('circleDiameter')
        copyInput    = inputs.itemById('numCopies')
        spacingInput = inputs.itemById('circleSpacing')
        
        if not selInput or not diaInput or not copyInput or not spacingInput:
            ui.messageBox('Fehler: Nicht alle Eingaben gefunden.')
            return
        
        if selInput.selectionCount != 1:
            ui.messageBox('Bitte genau einen Startpunkt auswählen.')
            return
        
        diameter = diaInput.value
        numCopies = copyInput.value
        spacing = spacingInput.value
        
        # Aktives Produkt prüfen (Fusion Design?)
        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('Bitte in einem aktiven Fusion-Design ausführen.')
            return
        
        # Aktive Skizze ermitteln
        activeSketch = None
        try:
            activeSketch = adsk.fusion.Sketch.cast(app.activeEditObject)
        except:
            pass
        if not activeSketch or not isinstance(activeSketch, adsk.fusion.Sketch):
            ui.messageBox("Keine aktive Skizze gefunden. Bitte in einer Skizze ausführen.")
            return
        
        # Koordinaten des ausgewählten Punkts
        startPointEntity = selInput.selection(0).entity
        pointGeom = getattr(startPointEntity, 'geometry', None)
        if not pointGeom:
            ui.messageBox("Der ausgewählte Punkt hat keine gültige Geometrie.")
            return
        
        baseX = pointGeom.x
        baseY = pointGeom.y
        radius = diameter / 2.0
        
        # Referenz auf SketchCircles
        sketchCircles = activeSketch.sketchCurves.sketchCircles
        
        # 1) Basiskreis am ausgewählten Punkt
        baseCircle = sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(baseX, baseY, 0),
            radius
        )
        
        # 2) Erzeuge eine lineare Anordnung in x-Richtung:
        #    => numCopies zusätzliche Kreise (plus Basiskreis = numCopies+1 insgesamt)
        linearCircles = [baseCircle]
        for i in range(1, numCopies + 1):
            offsetX = i * spacing
            centerPt = adsk.core.Point3D.create(baseX + offsetX, baseY, 0)
            c = sketchCircles.addByCenterRadius(centerPt, radius)
            linearCircles.append(c)
        
        # 3) Für jeden Kreis außer dem 1. (Basiskreis):
        #    -> erstelle eine runde (kreisförmige) Anordnung um den Basiskreis.
        #    Die Anzahl der Kreise in jeder Rund-Anordnung:
        #       beginnt bei 7 (2. Kreis in der Linie)
        #       und wird pro weiterem Kreis um 6 erhöht (d.h. 7, 13, 19, ...)
        
        # Basiskreis ist linearCircles[0].
        # Die "weiteren" Kreise sind linearCircles[1], [2], ...
        
        for i, circleObj in enumerate(linearCircles[1:], start=1):
            # i=1 -> 2. Kreis => 7 Kreise in der Anordnung
            # i=2 -> 3. Kreis => 13 Kreise ...
            # ...
            totalCircular = 7 + 6*(i-1)
            
            # Mittelpunkt des aktuellen Kreises in der Linie
            circleGeom = circleObj.centerSketchPoint.geometry
            cx = circleGeom.x
            cy = circleGeom.y
            
            # Wir fassen den Kreis selbst als "Teil der Anordnung" auf;
            # d.h. wir erzeugen totalCircular - 1 zusätzliche Kreise.
            angleStep = 2.0 * math.pi / totalCircular
            
            dx = cx - baseX
            dy = cy - baseY
            
            for k in range(1, totalCircular):
                angle = k * angleStep
                
                # Rotation in 2D um (baseX, baseY)
                rx = dx * math.cos(angle) - dy * math.sin(angle)
                ry = dx * math.sin(angle) + dy * math.cos(angle)
                
                newX = baseX + rx
                newY = baseY + ry
                
                # Neuer Kreis
                sketchCircles.addByCenterRadius(
                    adsk.core.Point3D.create(newX, newY, 0),
                    radius
                )
        
        ui.messageBox(
            f"Fertig!\n\n"
            f"- 1 Basiskreis + {numCopies} Kreise in x-Richtung.\n"
            f"- Für jeden dieser Kopien eine Rund-Anordnung (7, 13, 19, ...)."
        )