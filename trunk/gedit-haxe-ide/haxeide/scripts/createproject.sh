#!/bin/bash
#
# createProject.sh
# command = ["./createproject.sh", target, destinationFolder, folderName, main]

target=$1 #flash, neko, js, cpp, 
destinationFolder=$2 #/home/user/documents/projects
folderName=$3 #test
main=$4 # com.example.Main

mainPath=${main//.//} # com/example/Main
mainName=${main##*.} # Main

package=${main%.*} #com.example
packagePath=${package//.//} #com/example

	if [[ $package = $main ]]
		then 
		package=""
		packagePath=""
	fi
	

	mkdir -p $destinationFolder/$folderName/bin
	mkdir -p $destinationFolder/$folderName/src/$packagePath
	
	## Build.hxml aanpassingen (-main)
	cp $target'_project_template/build.hxml' $destinationFolder/$folderName/build.hxml
	sed -i "s/-main Main/-main $main/" $destinationFolder/$folderName/build.hxml
	
	## Main.hx aanpassingen (package and class name)
	cp $target'_project_template/src/Main.hx' $destinationFolder/$folderName/src/$mainPath.hx
	sed -i "s/package;/package $package;/" $destinationFolder/$folderName/src/$mainPath.hx
	sed -i "s/Main/$mainName/" $destinationFolder/$folderName/src/$mainPath.hx
	
	
