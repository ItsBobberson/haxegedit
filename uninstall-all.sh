#!/bin/sh
cd ./gedit-haxe-codecompletion
sh ./uninstall.sh

cd ../gedit-haxe-ide
sh ./uninstall.sh

cd ../gedit-haxe-syntaxhighlighting
sh ./uninstall.sh

cd ../gedit-codebrowser
sh ./uninstall.sh

cd ../ctags
sh ./uninstall.sh
