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
		if(args.length < 0)
		{
			Lib.println("Usage: neko application.n arg0, arg1...");
			Sys.exit(1);
		}
		var sum = Std.parseInt(args[0]) + Std.parseInt(args[1]);
		Lib.println(sum);
	}
	
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
}
