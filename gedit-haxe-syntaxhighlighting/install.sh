#!/bin/sh
LANGSPEC_FILE="haxe.lang"
MIME_FILE="haxe.xml"

ROOT_LANGSPEC_FOLDER="/usr/share/gtksourceview-3.0/language-specs"
ROOT_MIME_FOLDER="/usr/share/mime"
ROOT_MIME_PACKAGES_FOLDER="/usr/share/mime/packages"

USER_LANGSPEC_FOLDER="$HOME/.local/share/gtksourceview-3.0/language-specs"
USER_MIME_FOLDER="$HOME/.local/share/mime"
USER_MIME_PACKAGES_FOLDER="$HOME/.local/share/mime/packages"

if [ `whoami` = 'root' ]; then
	LANGSPEC_FOLDER=$ROOT_LANGSPEC_FOLDER
	MIME_FOLDER=$ROOT_MIME_FOLDER
	MIME_PACKAGES_FOLDER=$ROOT_MIME_PACKAGES_FOLDER
else
	LANGSPEC_FOLDER=$USER_LANGSPEC_FOLDER
	MIME_FOLDER=$USER_MIME_FOLDER
	MIME_PACKAGES_FOLDER=$USER_MIME_PACKAGES_FOLDER
fi

echo "*** Installing haXe syntax file for highlighting ***"

if [ ! -d $LANGSPEC_FOLDER ]; then
	mkdir -p "$LANGSPEC_FOLDER"
fi

if [ ! -d $MIME_PACKAGES_FOLDER ]; then
		mkdir -p "$MIME_PACKAGES_FOLDER"
fi


if [ ! -f "$MIME_PACKAGES_FOLDER/$MIME_FILE" ]; then
	echo "Adding file: $MIME_FILE, to: $MIME_PACKAGES_FOLDER"
	cp "$MIME_FILE" "$MIME_PACKAGES_FOLDER/$MIME_FILE"
fi
	
if [ ! -f "$LANGSPEC_FOLDER/$LANGSPEC_FILE" ]; then
	echo "Adding file: $LANGSPEC_FILE, to: $LANGSPEC_FOLDER"
	cp "$LANGSPEC_FILE" "$LANGSPEC_FOLDER/$LANGSPEC_FILE"
fi

echo "updating mime-database"
update-mime-database "$MIME_FOLDER"

echo "Done installing haxe syntax file.\n"
