#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

# Luxrender renderer for FreeCAD

# This file can also be used as a template to add more rendering engines.
# You will need to make sure your file is named with a same name (case sensitive)
# That you will use everywhere to describe your renderer, ex: Appleseed or Povray


# A render engine module must contain the following functions:
#
#    writeCamera(camdata): returns a string containing an openInventor camera string in renderer format
#    writeObject(view): returns a string containing a RaytracingView object in renderer format
#    render(project,external=True): renders the given project, external means if the user wishes to open
#                                   the render file in an external application/editor or not. If this
#                                   is not supported by your renderer, you can simply ignore it
#
# Additionally, you might need/want to add:
#
#    Preference page items, that can be used in your functions below
#    An icon under the name Renderer.svg (where Renderer is the name of your Renderer


import FreeCAD,math


def writeCamera(camdata):


    # this is where you create a piece of text in the format of
    # your renderer, that represents the camera. You can use the contents
    # of obj.Camera, which contain a string in OpenInventor format
    # ex:
    # #Inventor V2.1 ascii
    #
    #
    # PerspectiveCamera {
    #  viewportMapping ADJUST_CAMERA
    #  position 0 -1.3207401 0.82241058
    #  orientation 0.99999666 0 0  0.26732138
    #  nearDistance 1.6108983
    #  farDistance 6611.4492
    #  aspectRatio 1
    #  focalDistance 5
    #  heightAngle 0.78539819
    #
    # }
    #
    # or (ortho camera):
    #
    # #Inventor V2.1 ascii
    #
    #
    # OrthographicCamera {
    #  viewportMapping ADJUST_CAMERA
    #  position 0 0 1
    #  orientation 0 0 1  0
    #  nearDistance 0.99900001
    #  farDistance 1.001
    #  aspectRatio 1
    #  focalDistance 5
    #  height 4.1421356
    #
    # }

    if not camdata:
        return ""
    camdata = camdata.split("\n")
    cam = ""
    pos = [float(p) for p in camdata[5].split()[-3:]]
    pos = FreeCAD.Vector(pos)
    rot = [float(p) for p in camdata[6].split()[-4:]]
    rot = FreeCAD.Rotation(FreeCAD.Vector(rot[0],rot[1],rot[2]),math.degrees(rot[3]))
    tpos = pos.add(rot.multVec(FreeCAD.Vector(0,0,-1)))
    up = rot.multVec(FreeCAD.Vector(0,1,0))
    cam += "# declares position and view direction\n"
    cam += "# Generated by FreeCAD (http://www.freecadweb.org/)\n"
    cam += "LookAt " + str(pos.x) + " " + str(pos.y) + " " + str(pos.z) + " "
    cam += str(tpos.x) + " " + str(tpos.y) + " " + str(tpos.z) + " "
    cam += str(up.x) + " " + str(up.y) + " " + str(up.z) + "\n"
    return cam


def writeObject(viewobj):


    # This is where you write your object/view in the format of your
    # renderer. "obj" is the real 3D object handled by this project, not
    # the project itself. This is your only opportunity
    # to write all the data needed by your object (geometry, materials, etc)
    # so make sure you include everything that is needed

    if not viewobj.Source:
        return ""
    objdef = ""
    obj = viewobj.Source
    objname = viewobj.Name
    color = None
    alpha = None
    mat = None
    if viewobj.Material:
        mat = viewobj.Material
    else:
        if "Material" in obj.PropertiesList:
            if obj.Material:
                mat = obj.Material
    if mat:
        if "Material" in mat.PropertiesList:
            if "DiffuseColor" in mat.Material:
                color = mat.Material["DiffuseColor"].strip("(").strip(")").split(",")
                color = str(color[0])+" "+str(color[1])+" "+str(color[2])
            if "Transparency" in mat.Material:
                if float(mat.Material["Transparency"]) > 0:
                    alpha = str(1.0/float(mat.Material["Transparency"]))
                else:
                    alpha = "1.0"
    if obj.ViewObject:
        if not color:
            if hasattr(obj.ViewObject,"ShapeColor"):
                color = obj.ViewObject.ShapeColor[:3]
                color = str(color[0])+" "+str(color[1])+" "+str(color[2])
        if not alpha:
            if hasattr(obj.ViewObject,"Transparency"):
                if obj.ViewObject.Transparency > 0:
                    alpha = str(1.0/(float(obj.ViewObject.Transparency)/100.0))
    if not color:
        color = "1.0 1.0 1.0"
    if not alpha:
        alpha = "1.0"
    m = None
    if obj.isDerivedFrom("Part::Feature"):
        import MeshPart
        m = MeshPart.meshFromShape(Shape=obj.Shape, 
                                   LinearDeflection=0.1, 
                                   AngularDeflection=0.523599, 
                                   Relative=False)
    elif obj.isDerivedFrom("Mesh::Feature"):
        m = obj.Mesh
    if not m:
        return ""
    P = ""
    N = ""
    tris = ""
    for v in m.Topology[0]:
        P += str(v.x) + " " + str(v.y) + " " + str(v.z) + " "
    for n in m.getPointNormals():
        N += str(n.x) + " " + str(n.y) + " " + str(n.z) + " "
    for t in m.Topology[1]:
        tris += str(t[0]) + " " + str(t[1]) + " " + str(t[2]) + " "
        
    objdef += "MakeNamedMaterial \"" + objname + "_mat\"\n"
    objdef += "    \"color Kd\" [" + color + "]\n"
    objdef += "    \"float sigma\" [0.2]\n"
    objdef += "    \"string type\" [\"matte\"]\n"
    objdef += "\n"    
    objdef += "AttributeBegin #  \"" + objname + "\"\n"
    objdef += "Transform [1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1]\n"
    objdef += "NamedMaterial \"" + objname + "_mat\"\n"
    objdef += "Shape \"mesh\"\n"
    objdef += "    \"integer triindices\" [" + tris + "]\n"
    objdef += "    \"point P\" [" + P + "]\n"
    objdef += "    \"normal N\" [" + N + "]\n"
    objdef += "    \"bool generatetangents\" [\"false\"]\n"
    objdef += "    \"string name\" [\"" + objname + "\"]\n"
    objdef += "AttributeEnd # \"\"\n"

    return objdef


def render(project,external=True):


    if not project.PageResult:
        return
    p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Render")
    if external:
        rpath = p.GetString("LuxRenderPath","")
        args = ""
    else:
        rpath = p.GetString("LuxConsolePath","")
        args = p.GetString("LuxParameters","")
    if not rpath:
        raise
    if args:
        args += " "
    import os
    os.system(rpath+" "+args+project.PageResult)
    return


