import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

# Version History
# 1.0.1 - 2020-07-03: Made it so if you don't have Add or Subtract selected (say, Mix) it'll try to set the brush to Add.
# 1.0.2 - 2020-11-11: This now affects texture painting brushes, not just weight painting brushes. Changed the name of this from "Toggle Weight Painting Brush Blend" to "Toggle Add Subtract Brush Blend" since it's no longer exclusively for weight painting.
# 1.0.3 - 2020-12-16: Sends back an INFO message when launched. I needed to see some user feedback to make sure this was actually being launched.
# 1.0.4 - 2020-12-17: Figured out how to switch ONLY the current brush, rather than all brushes.

# 1.1.0 - 2026-02-06: Added Sculpt Mode dirciton, removed add/sub mode for weight paint and tetxure paint (I use mix mode), Added toggles for front face only and projection


bl_info = {
    "name": "Expanded Brush Utilities",
    "author": "Zaytha, Jeff Boller",
    "version": (1, 1, 0),
    "blender": (5, 00, 1),
    "location": "",
    "description": "Adds hotkeys for toggling brush direction (sculpt only), front faces only, and falloff shape",
    "wiki_url": "",
    "tracker_url": "https://github.com/Zaytha/ExpandedBrushUtilities",
    "category": "System"}


# Toggling brush mode
# I removed the add / sub mode for weight painting / texture painting as I use the mix mode 
class WM_OT_toggle_sculpt_direction_blend(bpy.types.Operator):
    bl_idname = "wm.toggle_sculpt_direction_blend"
    bl_label = "Toggle Sculpt Direction"
    bl_description = "Toggles direction of sculpting burushes."


    def execute(self, context):
        brush = None
        mode_name = ""
        
        if context.mode == "SCULPT":
            brush = context.tool_settings.sculpt.brush
            mode_name = "Sculpt"
        
        if brush and brush.direction != "DEFAULT":
            positive_direction = "ADD"
            negative_direction = "SUBTRACT"

            # Crusty fix becuase I coudln't get the enum values for custom brushed idkkkkk
            if brush.name == "Inflate/Deflate":
                positive_direction = "INFLATE"
                negative_direction = "DEFLATE"
            elif brush.name == "Smooth":
                positive_direction = "SMOOTH"
                negative_direction = "ENHANCE_DETAILS"
            elif brush.name == "Pinch/Magnify":
                positive_direction = "MAGNIFY"
                negative_direction = "PINCH"


            if brush.direction == positive_direction:
                brush.direction = negative_direction
                self.report({"INFO"}, f"{mode_name} - Direction: {negative_direction}")
            else:
                brush.direction = positive_direction
                self.report({"INFO"}, f"{mode_name} - Direction: {positive_direction}")
        else:
            self.report({"WARNING"}, "No active brush or unsupported mode")
        
        return {"FINISHED"}

# Change if this tool should only effect normals that are facing you
class WM_OT_toggle_front_faces_only(bpy.types.Operator):
    bl_idname = "wm.toggle_front_faces_only"
    bl_label = "Toggle Front Faces Only"
    bl_description = "Toggle Front Facing Only option for brush"

    def execute(self, context):
        brush = None
        mode_name = ""
        
        if context.mode == "SCULPT":
            brush = context.tool_settings.sculpt.brush
            mode_name = "Sculpt"
        elif context.mode == "PAINT_WEIGHT":
            brush = context.tool_settings.weight_paint.brush
            mode_name = "Weight Paint"
        elif context.mode == "PAINT_TEXTURE":
            brush = context.tool_settings.image_paint.brush
            mode_name = "Texture Paint"
        
        if brush:
            brush.use_frontface = not brush.use_frontface
            state = "ON" if brush.use_frontface else "OFF"
            self.report({"INFO"}, f"{mode_name} - Front Faces Only: {state}")
        else:
            self.report({"WARNING"}, "No active brush or unsupported mode")
        
        return {"FINISHED"}

# Change falloff to be sphere around drawing point or projected htourhgout the mesh
class WM_OT_toggle_falloff_shape(bpy.types.Operator):
    bl_idname = "wm.toggle_falloff_shape"
    bl_label = "Toggle Falloff Shape"
    bl_description = "Toggle between Sphere and Projected falloff shape"

    def execute(self, context):
        brush = None
        mode_name = ""
        
        if context.mode == "SCULPT":
            brush = context.tool_settings.sculpt.brush
            mode_name = "Sculpt"
        elif context.mode == "PAINT_WEIGHT":
            brush = context.tool_settings.weight_paint.brush
            mode_name = "Weight Paint"
        elif context.mode == "PAINT_TEXTURE":
            brush = context.tool_settings.image_paint.brush
            mode_name = "Texture Paint"
        
        if brush:
            if brush.falloff_shape == "SPHERE":
                brush.falloff_shape = "PROJECTED"
                self.report({"INFO"}, f"{mode_name} - Falloff Shape: Projected")
            else:
                brush.falloff_shape = "SPHERE"
                self.report({"INFO"}, f"{mode_name} - Falloff Shape: Sphere")
        else:
            self.report({"WARNING"}, "No active brush or unsupported mode")
        
        return {"FINISHED"}

class ExpandedBrushUtilitiesPreferences(AddonPreferences):
    bl_idname = __name__
    
    def draw(self, context):
        layout = self.layout

        # Description
        layout.label(text="Expanded Brush Utilities")
        layout.separator()
        layout.label(text="Adds hotkeys for toggling brush direction (sculpt only), front faces only, and falloff shape")
        layout.label(text="Re-Written version of Jeff Boller's 'Toggle Add Subtract Brush Blend' script.")
        layout.label(text="Github: https://github.com/Zaytha/ExpandedBrushUtilities")
        layout.label(text="Original code: https://blenderartists.org/t/weight-painting-toggle-between-add-and-subtract/1161121/13")

        # no idea if there's like, a block of code editor in blender but this works idkkkkkkk
        layout.separator()
        layout.label(text="Features:")
        layout.label(text="- Toggles direction of brush (sculpting only)")
        layout.label(text="- Toggles front facing only option")
        layout.label(text="- Toggles falloff mode from sphere to projection")
        layout.separator()
        layout.label(text="Default Keybinds:")
        layout.label(text="- Toggle Sculpt Direction (Ctrl + Shift + H)")
        layout.label(text="- Toggle Front Facing Only (Ctrl + Shift + J)")
        layout.label(text="- Toggle Falloff Shape (Ctrl + Shift + K)")
        layout.separator()

def register():
    bpy.utils.register_class(WM_OT_toggle_sculpt_direction_blend)
    bpy.utils.register_class(WM_OT_toggle_front_faces_only)
    bpy.utils.register_class(WM_OT_toggle_falloff_shape)
    bpy.utils.register_class(ExpandedBrushUtilitiesPreferences)

    # keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # sculpt
        km = kc.keymaps.new(name="Sculpt", space_type="EMPTY")
        
        kmi = km.keymap_items.new("wm.toggle_sculpt_direction_blend", "H", "PRESS", ctrl = True, shift=True)
        kmi = km.keymap_items.new("wm.toggle_front_faces_only", "J", "PRESS", ctrl = True, shift=True)
        kmi = km.keymap_items.new("wm.toggle_falloff_shape", "K", "PRESS", ctrl = True, shift=True)
        
        # weight paint
        km = kc.keymaps.new(name="Weight Paint", space_type="EMPTY")
        
        kmi = km.keymap_items.new("wm.toggle_front_faces_only", "J", "PRESS", ctrl = True, shift=True)
        kmi = km.keymap_items.new("wm.toggle_falloff_shape", "K", "PRESS", ctrl = True, shift=True)
        
        # textur paint
        km = kc.keymaps.new(name="Image Paint", space_type="EMPTY")
        
        kmi = km.keymap_items.new("wm.toggle_front_faces_only", "J", "PRESS", ctrl = True, shift=True)
        kmi = km.keymap_items.new("wm.toggle_falloff_shape", "K", "PRESS", ctrl = True, shift=True)

def unregister():
    bpy.utils.unregister_class(WM_OT_toggle_sculpt_direction_blend)
    bpy.utils.unregister_class(WM_OT_toggle_front_faces_only)
    bpy.utils.unregister_class(WM_OT_toggle_falloff_shape)
    bpy.utils.unregister_class(ExpandedBrushUtilitiesPreferences)

    # remove keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if kmi.idname in ["wm.toggle_sculpt_direction_blend", "wm.toggle_front_faces_only", "wm.toggle_falloff_shape"]:
                    km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()
