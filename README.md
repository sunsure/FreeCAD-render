# Render workbench

A [FreeCAD](http://www.freecadweb.org) workbench to produce high-quality rendered images from your FreeCAD document, using open-source external rendering engines

## Introduction

The Render workbench is a replacement for the built-in [Raytracing workbench](https://www.freecadweb.org/wiki/Raytracing_Module) of FreeCAD. There are several differences between the two:

* The Render workbench is fully written in Python, which makes it much easier to understand and extend by non-C++ programmers
* It is intentionally very simple to read, understand and modify (one file which provides common classes and methods for all renderers, and one file for each renderer)
* Adding new render engines (renderers) is very easy
* Like the builtin Raytracing workbench, the Render workbench offers the possibility to update the View objects whenever its source object changes, which costs extra processing time everytime the source object changes, but it also offers a mode where the views are updated all at once, only when the render is performed. This makes the render slower, but adds virtually no slowdown during the work with FreeCAD, no matter the size of a Render project.
* The Render workbench uses the same [templates](https://www.freecadweb.org/wiki/Raytracing_Module#Templates) as the Raytracing workbench, they are fully compatible. Appleseed templates are created the same way (check the [default template](templates/empty.appleseed) for example)

## Supported render engines

At the moment, the following engines are supported:

* Pov-Ray http://povray.org/
* Luxrender http://www.luxrender.net/
* Appleseed http://appleseedhq.net/

## Installation

The Render workbench is part of the [Addons repository](https://github.com/FreeCAD/FreeCAD-addons), and can be installed from menu Tools->Addon Manager in FreeCAD >= 0.17 or using the Addon Installer macro (see repository above) in earlier versions. It can also be installed manually by downloading this repository using the "clone or download" button above. Refer to the [FreeCAD documentation](https://www.freecadweb.org/wiki/How_to_install_additional_workbenches) to learn more.

## Usage

The Render workbench works exactly the same way as the [Raytracing Workbench](https://www.freecadweb.org/wiki/Raytracing_Module). You start by creating a Render project using one of the Renderer buttons from the Render Workbench toolbar, then select some of your document objects, and add views of these objects to your Render project, using the Add View button. You can tweak some features of the views (color, transparency, etc) if you want it to appear differently in the render than in the 3D view of FreeCAD, then, with a Render project selected, you only need to press the Render button to start the render.

Each renderer has some configurations to be set in Edit -> Preferences -> Render before being able to use it, namely the path to its executable.

## To Do

* Currently the external (open the file to be rendered in the Renderer's GUI)/internal (render directly inside FreeCAD) render mode is not implemented, the external mode will always be used.
* Add support for Kerkythea (adapt the existing macro)
* Add support for Blender's Eevee
* Add support for OpenCasCade's CadRays https://www.opencascade.com/content/cadrays

