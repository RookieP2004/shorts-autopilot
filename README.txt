Large build dependencies for shorts-autopilot (not code).
Blender as a Python module (bpy 5.2.3, GPL) wheel, split into <100 MB parts.
Rebuild: cat bpy-*.part* > bpy-5.2.3-cp313-cp313-manylinux_2_28_x86_64.whl && sha256sum -c SHA256SUMS
