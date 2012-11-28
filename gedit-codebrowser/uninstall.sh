#!/bin/sh

#user paths
USER_GEDIT_PLUGINS_FOLDER="$HOME/.local/share/gedit/plugins"

#root paths
ROOT_GEDIT_SCHEMAS_FOLDER="/usr/share/glib-2.0/schemas"
ROOT_GEDIT_PLUGINS_FOLDER="/usr/lib/gedit/plugins"

remove_file() 
{
	if [ -f $2/$1 ]; then
		echo "Removing file: $1, from: $2"
		rm $2/$1 || exit 1
	fi
}

remove_folder() 
{
	if [ -d $2/$1 ]; then
		echo "Removing folder: $1, from: $2"
		rm -r $2/$1 || exit 1
	fi
}

echo "*** Uninstalling code browser plugin for gedit 3.x ***"
if [ `whoami` = 'root' ]; then
	remove_file 'org.gnome.gedit.plugins.sourcecodebrowser.gschema.xml' "$ROOT_GEDIT_SCHEMAS_FOLDER"
	remove_file 'sourcecodebrowser.plugin' "$ROOT_GEDIT_PLUGINS_FOLDER"
	remove_folder 'sourcecodebrowser' "$ROOT_GEDIT_PLUGINS_FOLDER"
	echo "Recompiling: glib-compile-schemas"
	glib-compile-schemas "$ROOT_GEDIT_SCHEMAS_FOLDER"
else
	remove_file 'sourcecodebrowser.plugin' "$USER_GEDIT_PLUGINS_FOLDER"
	remove_folder 'sourcecodebrowser' "$USER_GEDIT_PLUGINS_FOLDER"
fi

echo "Done uninstalling ctags for haXe.\n"

