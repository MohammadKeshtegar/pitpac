import PyInstaller.__main__
import os
import platform

# Define the project details
main_script = "windows/pitpac.py"
app_name = "Pitpac"
icon_path = "windows/assets/app-icon.png"  # Adjust based on your structure

project_root = os.path.dirname(os.path.abspath( __file__))

# Define files to include with --add-data
# Format: (source_path, destination_path)
data_files = [
    (os.path.join(project_root, "windows/styles/base.css"), "windows/styles"),
    (os.path.join(project_root, "windows/styles/video_size_reducer.css"), "windows/styles"),
    (os.path.join(project_root, "windows/assets/plus-bold-dark.svg"), "assets"),
    (os.path.join(project_root, "windows/assets/minus-bold-dark.svg"), "assets"),
    (os.path.join(project_root, "windows/assets/x-dark.svg"), "assets"),
    (os.path.join(project_root, "windows/assets/folder-simple-fill-dark.svg"), "assets"),
    (os.path.join(project_root, "windows/assets/app-icon.png"), "assets"),
    (os.path.join(project_root, ".env"), ".")
]

# Platform-specific separator for --add-data
separator = ";" if platform.system() == "Windows" else ":"

# Construct PyInstaller arguments
pyinstaller_args = [
    main_script,
    "--name", app_name,
    "--onefile",
    "--windowed",
    "--noconfirm",
]

# Add icon if specified
if os.path.exists(icon_path):
    pyinstaller_args.extend(["--icon", icon_path])

# Add data files
for src, dst in data_files:
    pyinstaller_args.append(f"--add-data={src}{separator}{dst}")

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print(f"Build completed! Executable is located in the 'dist' directory.")