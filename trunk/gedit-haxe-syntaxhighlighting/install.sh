#!/bin/sh

ROOT_LANGSPEC_FOLDER="/usr/share/gtksourceview-3.0/language-specs"
ROOT_MIME_FOLDER="/usr/share/mime"
ROOT_MIME_PACKAGES_FOLDER="/usr/share/mime/packages"

USER_LANGSPEC_FOLDER="$HOME/.local/share/gtksourceview-3.0/language-specs"
USER_MIME_FOLDER="$HOME/.local/share/mime"
USER_MIME_PACKAGES_FOLDER="$HOME/.local/share/mime/packages"

LANGSPEC_FILE="haxe.lang"
MIME_FILE="haxe.xml"

echo "\n*** Installing haXe syntax file for highlighting ***\n"

#create directories for the plugin files
if [ `whoami` != 'root' ]; then

	if [ ! -d $USER_LANGSPEC_FOLDER ]; then
		mkdir -p "$USER_LANGSPEC_FOLDER"
	fi
	
	if [ ! -d $USER_MIME_PACKAGES_FOLDER ]; then
		mkdir -p "$USER_MIME_PACKAGES_FOLDER"
	fi
	
fi


if [ `whoami` = 'root' ]; then

	if [ ! -f "$ROOT_MIME_PACKAGES_FOLDER/$MIME_FILE" ]; then
		echo "Adding $MIME_FILE to $ROOT_MIME_PACKAGES_FOLDER"
		cp "$MIME_FILE" "$ROOT_MIME_PACKAGES_FOLDER/$MIME_FILE"
	fi
	
	if [ ! -f "$ROOT_LANGSPEC_FOLDER/$LANGSPEC_FILE" ]; then
		echo "Adding $LANGSPEC_FILE to $ROOT_LANGSPEC_FOLDER"
		cp "$LANGSPEC_FILE" "$ROOT_LANGSPEC_FOLDER/$LANGSPEC_FILE"
	fi
	echo "updating mime-database"
	update-mime-database "$ROOT_MIME_FOLDER"
	
else

	if [ ! -f "$USER_MIME_PACKAGES_FOLDER/$MIME_FILE" ]; then
		echo "Adding $MIME_FILE to $USER_MIME_PACKAGES_FOLDER"
		cp "$MIME_FILE" "$USER_MIME_PACKAGES_FOLDER/$MIME_FILE"
	fi
	
	if [ ! -f "$USER_LANGSPEC_FOLDER/$LANGSPEC_FILE" ]; then
		echo "Adding $LANGSPEC_FILE to $USER_LANGSPEC_FOLDER"
		cp "$LANGSPEC_FILE" "$USER_LANGSPEC_FOLDER/$LANGSPEC_FILE"
	fi
	echo "updating mime-database"
	update-mime-database "$USER_MIME_FOLDER"

fi

echo "\nDone installing.\n"
