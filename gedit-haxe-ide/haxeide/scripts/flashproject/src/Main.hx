package;
import flash.display.MovieClip;

class Main extends MovieClip
{
	public function new()
	{
		super();
		trace("test");
	}
	public static function main()
	{
		flash.Lib.current.stage.scaleMode=flash.display.StageScaleMode.NO_SCALE;
		flash.Lib.current.stage.align=flash.display.StageAlign.TOP_LEFT;
		flash.Lib.current.addChild(new Main());
	}
}
