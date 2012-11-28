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
	#mkdir -p $destinationFolder/$folderName/bin
	mkdir -p $destinationFolder/$folderName/src/$packagePath
	
	## copy bin folder
	cp -r $target'_project_template/bin' $destinationFolder/$folderName
	
	## build.hxml (adjust-main) and run.sh
	cp $target'_project_template/run.sh' $destinationFolder/$folderName/run.sh
	cp $target'_project_template/build.hxml' $destinationFolder/$folderName/build.hxml
	sed -i "s/-main Main/-main $main/" $destinationFolder/$folderName/build.hxml
	
	## Main.hx (adjust package and class name)
	cp $target'_project_template/src/Main.hx' $destinationFolder/$folderName/src/$mainPath.hx
	sed -i "s/package;/package $package;/" $destinationFolder/$folderName/src/$mainPath.hx
	sed -i "s/Main/$mainName/" $destinationFolder/$folderName/src/$mainPath.hx
	
	
