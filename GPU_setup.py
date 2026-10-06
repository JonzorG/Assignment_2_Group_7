import bpy

"""This code was generated with google gemini"""
import bpy

def enable_gpus(device_type):
    # 1. Access the Cycles preferences
    preferences = bpy.context.preferences
    cycles_prefs = preferences.addons["cycles"].preferences
    
    # 2. Set the compute API first (e.g., 'CUDA', 'OPTIX', 'HIP', 'METAL', 'ONEAPI')
    cycles_prefs.compute_device_type = device_type
    
    # 3. Force Blender to refresh the internal list of available hardware
    cycles_prefs.get_devices()
    
    activated_gpus = []
    
    # 4. Iterate through the updated devices collection
    for device in cycles_prefs.devices:
        if device.type != 'CPU':
            device.use = True
            activated_gpus.append(device.name)
        else:
            device.use = False # Disable CPU to force strict GPU rendering

    # 5. Tell the current scene to use the GPU compute backend
    bpy.context.scene.cycles.device = 'GPU'
    
    return activated_gpus

print(enable_gpus('CUDA'))
