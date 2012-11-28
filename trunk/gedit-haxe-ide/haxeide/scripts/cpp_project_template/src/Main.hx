package;
import cpp.FileSystem;
import cpp.Lib;
import cpp.Sys;
import cpp.io.Bytes;
import cpp.io.File;

class Main
{
	static var args:Array<String>;
	
	public static function main()
	{
		args = Sys.args();
		if(args.length < 2)
		{
			Lib.println("Usage: neko application.n arg0, arg1...");
			Sys.exit(1);
		}
		var sum = Std.int(args[0]) + Std.int(args[0]);
		Lib.println(sum);
	}
	
	/*
	//read or write text or binary files:
	
	static function handleFiles():Void
	{
		//if (FileSystem.exists(path))
		var str:String = File.getContent("fileA.txt");
		var fhs = File.write("fileB.txt", false);
		fhs.writeString(str);
		fhs.close();
		
		var bin:Bytes = File.getBytes("fileA.bin");
		var fhb = File.write("fileB.bin", true);
		fhb.write(bin);
		fhb.close();
	}
	*/
}
