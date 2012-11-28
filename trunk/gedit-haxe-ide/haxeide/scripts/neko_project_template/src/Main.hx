package;
import neko.FileSystem;
import neko.Lib;
import neko.Sys;
import haxe.io.Bytes;
import neko.io.File;

class Main
{
	static var args:Array<String>;
	
	public static function main()
	{
		args = Sys.args();
		if(args.length==0)
		{
			Lib.println("Usage: neko application.n arg0, arg1...");
			Sys.exit(1);
		}
		Lib.println(args[0] + " "+args[1]);
		
		//rest of code for this application...
	}
	
	
	//snippets
	
	//read or write text or binary files:
	static function handleFiles():Void
	{
		var str:String = File.getContent("fileA.txt");
		var fhs = File.write("fileB.txt", false);
		fhs.writeString(str);
		fhs.close();
		
		var bin:Bytes = File.getBytes("fileA.bin");
		var fhb = File.write("fileB.bin", true);
		fhb.write(bin);
		fhb.close();
	}
	static function fileExists(p:String)
	{
		if (!FileSystem.exists(p))
		{
			Lib.println("ERROR: File " + p + " could not be found.");
			Sys.exit(1);
		}
	}
	
	//Handle commandline arguments:
	static function argExists(v:String):Bool
	{
		for (arg in args)
			if (arg == v)
				return true;
		return false;
	}
	static function getArgValue(v:String):Null<String>
	{
		for (i in 0...args.length)
			if (args[i] == v)
				return args[i + 1];
		return null;
	}
	static function getExtension(str:String):String
	{
		return str.substr(str.lastIndexOf('.') + 1).toLowerCase();
	}
}
