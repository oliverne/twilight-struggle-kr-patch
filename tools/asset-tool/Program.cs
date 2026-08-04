using AssetsTools.NET;
using AssetsTools.NET.Extra;

// 용도: Unity 에셋 파일 탐색/덤프 (Phase 1 실험 B 준비)
// 사용법:
//   dotnet run -- probe <assets파일>                   # 파싱 진단 (헤더/타입)
//   dotnet run -- types <assets파일>                   # 클래스 타입 요약
//   dotnet run -- list  <assets파일>                   # TextAsset 이름/크기/PathId
//   dotnet run -- dump  <assets파일> <이름> [출력파일]    # TextAsset 본문 덤프

if (args.Length < 2)
{
    Console.Error.WriteLine("사용법: probe|types|list|dump <assets파일> [이름] [출력파일]");
    return 1;
}

string cmd = args[0];
string assetsPath = Path.GetFullPath(args[1]);
var am = new AssetsManager();
var af = am.LoadAssetsFile(assetsPath, true);
const long TEXT_ASSET_ID = 49;

bool IsTextAsset(AssetFileInfo inf) => inf.TypeIdOrIndex == TEXT_ASSET_ID || inf.ClassId == TEXT_ASSET_ID;

switch (cmd)
{
    case "probe":
    {
        int i = 0;
        foreach (var inf in af.file.AssetInfos)
        {
            Console.WriteLine($"PathId={inf.PathId} ClassId={inf.ClassId} TypeIdOrIndex={inf.TypeIdOrIndex} ScriptTypeIndex={inf.ScriptTypeIndex} Size={inf.ByteSize}");
            if (++i >= 15) break;
        }
        Console.WriteLine($"총 에셋: {af.file.AssetInfos.Count}");
        return 0;
    }
    case "types":
    {
        var counts = new Dictionary<long, int>();
        foreach (var inf in af.file.AssetInfos)
            counts[inf.TypeIdOrIndex] = counts.GetValueOrDefault(inf.TypeIdOrIndex) + 1;
        foreach (var kv in counts.OrderByDescending(kv => kv.Value))
        {
            string name = kv.Key >= 0 && Enum.IsDefined(typeof(AssetClassID), (int)kv.Key)
                ? ((AssetClassID)kv.Key).ToString() : "?";
            Console.WriteLine($"{kv.Value}\t{kv.Key}\t{name}");
        }
        return 0;
    }
    case "list":
    {
        foreach (var inf in af.file.AssetInfos)
        {
            if (!IsTextAsset(inf)) continue;
            var baseField = am.GetBaseField(af, inf);
            string name = baseField.Get("m_Name").AsString;
            long size = baseField.Get("m_Script").AsByteArray.LongLength;
            Console.WriteLine($"{inf.PathId}\t{size}\t{name}");
        }
        return 0;
    }
    case "dump":
    {
        if (args.Length < 3) { Console.Error.WriteLine("dump는 이름 필요"); return 1; }
        string name = args[2];
        foreach (var inf in af.file.AssetInfos)
        {
            if (!IsTextAsset(inf)) continue;
            var baseField = am.GetBaseField(af, inf);
            if (baseField.Get("m_Name").AsString != name) continue;
            byte[] data = baseField.Get("m_Script").AsByteArray;
            if (args.Length >= 4)
            {
                File.WriteAllBytes(args[3], data);
                Console.WriteLine($"{data.Length} 바이트 → {args[3]}");
            }
            else Console.WriteLine(System.Text.Encoding.UTF8.GetString(data));
            return 0;
        }
        Console.Error.WriteLine($"TextAsset '{name}' 없음");
        return 1;
    }
    default:
        Console.Error.WriteLine("알 수 없는 명령: " + cmd);
        return 1;
}
