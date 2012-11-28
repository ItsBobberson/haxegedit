#!/bin/sh
#
# Installs the haxe code completion plugin for user or root

#user paths
USER_GEDIT_PLUGINS_FOLDER="$HOME/.local/share/gedit/plugins"
USER_ICONS_FOLDER="$HOME/.local/share/icons"

#root paths
ROOT_GEDIT_SCHEMAS_FOLDER="/usr/share/glib-2.0/schemas"
ROOT_GEDIT_PLUGINS_FOLDER="/usr/lib/gedit/plugins"
ROOT_ICONS_FOLDER="/usr/share/icons"

#create directories for the plugin files
if [ `whoami` != 'root' ]; then
	mkdir -p "$USER_GEDIT_PLUGINS_FOLDER"
	mkdir -p "$USER_ICONS_FOLDER"
fi

#install a file
copy_file() 
{
	echo "Adding file $1 to $2"
	cp "$1" "$2" || exit 1
}

#install a folder
copy_folder() 
{
	echo "Adding folder $1 to $2"
	cp -r "$1" "$2" || exit 1
}

# Start installing haxe code completion plugin by copying the files to the correct folders
echo "\nInstalling haXe codecompletion plugin for GEdit 3.x\n"

if [ `whoami` = 'root' ]; then
	copy_file 'haxeide.plugin' "$ROOT_GEDIT_PLUGINS_FOLDER"
	copy_folder 'haxeide' "$ROOT_GEDIT_PLUGINS_FOLDER"
	echo "Recompiling: glib-compile-schemas"
	glib-compile-schemas "$ROOT_GEDIT_SCHEMAS_FOLDER"
else
	copy_file 'haxeide.plugin' "$USER_GEDIT_PLUGINS_FOLDER"
	copy_folder 'haxeide' "$USER_GEDIT_PLUGINS_FOLDER"
fi

echo '\n*** Restart GEdit to complete the installation for the haXe codecompletion plugin. ***\n'

