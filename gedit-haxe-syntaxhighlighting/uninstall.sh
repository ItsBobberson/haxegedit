#!/bin/sh

ROOT_LANGSPEC_FOLDER="/usr/share/gtksourceview-3.0/language-specs"
ROOT_MIME_FOLDER="/usr/share/mime"
ROOT_MIME_PACKAGES_FOLDER="/usr/share/mime/packages"

USER_LANGSPEC_FOLDER="$HOME/.local/share/gtksourceview-3.0/language-specs"
USER_MIME_FOLDER="$HOME/.local/share/mime"
USER_MIME_PACKAGES_FOLDER="$HOME/.local/share/mime/packages"

LANGSPEC_FILE="haxe.lang"
MIME_FILE="haxe.xml"

echo "*** Uninstalling haXe syntax files for highlighting ***"

if [ `whoami` = 'root' ]; then

	if [ -f "$ROOT_MIME_PACKAGES_FOLDER/$MIME_FILE" ]; then
		echo "Removing $MIME_FILE, from: $ROOT_MIME_PACKAGES_FOLDER"
		rm "$ROOT_MIME_PACKAGES_FOLDER/$MIME_FILE"
		echo "updating mime-database"
		update-mime-database "$ROOT_MIME_FOLDER"
	fi
	
	if [ -f "$ROOT_LANGSPEC_FOLDER/$LANGSPEC_FILE" ]; then
		echo "Removing $LANGSPEC_FILE, from: $ROOT_LANGSPEC_FOLDER"
		rm "$ROOT_LANGSPEC_FOLDER/$LANGSPEC_FILE"
	fi
	
	
else

	if [ -f "$USER_MIME_PACKAGES_FOLDER/$MIME_FILE" ]; then
		echo "Removing $MIME_FILE, from: $USER_MIME_PACKAGES_FOLDER"
		rm "$USER_MIME_PACKAGES_FOLDER/$MIME_FILE"
		echo "updating mime-database"
		update-mime-database "$USER_MIME_FOLDER"
	fi
	
	if [ -f "$USER_LANGSPEC_FOLDER/$LANGSPEC_FILE" ]; then
		echo "Removing $LANGSPEC_FILE, from: $USER_LANGSPEC_FOLDER"
		rm "$USER_LANGSPEC_FOLDER/$LANGSPEC_FILE"
	fi
fi

echo "Done uninstalling.\n"
