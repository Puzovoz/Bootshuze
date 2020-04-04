# Bootshuze
OBJ to XML converter for Spiral Knights

## Features

The script will:
  - Convert OBJ file's indices and vertices to XML format Spiral Knights uses.
  - Recognize the primitives mode the input file uses (lines, triangles, quads).
  - Calculate bounds for the model.
 
The script will NOT:
  - Change any data that can be changed with SpiralSpy after creation (material, texture, etc).
  - Normalize the model size. If the model is too big, you can scale it down in SpiralSpy by creating a new Compound model and using the model you just created as one of the assets.
  - Rotate the model. Can also be fixed by creating a Compound model.
  - Create new texture UV mapping. That should be done in any 3D model editor you're using.
  
## Getting started
  1. Download the latest release, and open either the .exe file or the .py file (the latter requires Python 3 installed).
  1. A console window should appear. When asked, provide the name of the OBJ model inside the script directory.
  1. The script should create an XML file inside the directory.
  1. With [SpiralSpy](https://www.lucasallegri.xyz/download/spiralspy-1.5.jar) open Resource Editor (Ctrl+R), `File → Import from XML...` and point to the new XML you created with the script. That should provide info to the resource editor.
  1. That model should now be saved (Ctrl+A) in any directory and opened in the model viewer.
  
  Congratulations, you've imported a model and can create new mods with new models that never existed in the game before.
