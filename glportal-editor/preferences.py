import bpy
import os
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty, StringProperty

from .operatorHelpers import itemsMaterial
from .preferencesHelper import updateTriggerXrays, updateSmartTexturesMapping, updateDefaultMaterial

class preferences(AddonPreferences):
  bl_idname = __package__

  triggerXrays = BoolProperty (
    name = "Use X-Rays for triggers",
    description = "Enable / Disable X-rays for triggers.",
    default = True,
    update = updateTriggerXrays
  )
  smartTexturesMapping = BoolProperty (
    name = "Smart textures mapping",
    description = "Calculate position of each texture.",
    default = True,
    update = updateSmartTexturesMapping
  )
  dataDir = StringProperty (
    name = "Set up GlPortal data directory",
    default = os.path.expanduser("~/.glportal/data/"),
    subtype = 'DIR_PATH'
  )
  gameExe = StringProperty (
    name = "Set up GlPortal executable",
    default = os.path.expanduser("/usr/bin/glportal"),
    subtype = 'FILE_PATH'
  )
  useDefaultMaterial = BoolProperty (
    name = "Assign default material to models",
    default = True
  )
  defaultMaterial = StringProperty (
    default = "boxes/dev00"
  )
  materials = EnumProperty (
    name = "Default material",
    items = itemsMaterial,
    update = updateDefaultMaterial
  )

  def draw(self, context):
    prefs = context.user_preferences.addons[__package__].preferences
    layout = self.layout

    layout.prop(self, "triggerXrays")
    layout.prop(self, "smartTexturesMapping")

    layout.prop(self, "useDefaultMaterial")
    if prefs.useDefaultMaterial:
      self.materials = self.defaultMaterial
      layout.prop(self, "materials")

    layout.prop(self, "dataDir")
    if os.path.isdir(os.path.expanduser(prefs.dataDir)) == False:
      layout.label(text="Current data directory does not exist", icon='ERROR')

    layout.prop(self, "gameExe")
    if os.path.isfile(os.path.expanduser(prefs.gameExe)) == False:
      layout.label(text="Current GlPortal executable does not exist", icon='ERROR')
