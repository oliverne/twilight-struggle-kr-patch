using System.Text.Json;
using AssetsTools.NET;
using AssetsTools.NET.Extra;

// 용도: Unity 에셋 파일 탐색/덤프/TextAsset 교체 (Phase 1 실험 B + Phase 4 재구축)
// 사용법:
//   dotnet run -- probe <assets파일>                     # 파싱 진단 (헤더/타입)
//   dotnet run -- types <assets파일>                     # 클래스 타입 요약
//   dotnet run -- list  <assets파일>                     # TextAsset 이름/크기/PathId
//   dotnet run -- dump  <assets파일> <이름> [출력파일]     # TextAsset 본문 덤프
//   dotnet run -- apply <assets파일> <plan.json> [출력]   # plan의 TextAsset 교체 후 저장
//
// AT2(AssetsTools.NET 2.0.12 NuGet) API 기준.
// 저장은 AssetsReplacerFromMemory로 수정 객체만 교체 — 나머지 객체는 원본 raw 보존 (m_Script 무손상)

const int TEXT_ASSET_ID = 49;

if (args.Length < 2)
{
    Console.Error.WriteLine("사용법: probe|types|list|dump|apply <assets파일> ...");
    return 1;
}

string cmd = args[0];
string assetsPath = Path.GetFullPath(args[1]);
var am = new AssetsManager();
var af = am.LoadAssetsFile(assetsPath, true);
var infos = af.table.assetFileInfo;

int GetClassId(AssetFileInfoEx inf)
{
    // curFileTypeOrIndex가 타입 트리 인덱스면 타입 트리에서 classId 조회
    if (af.file.typeTree.hasTypeTree && inf.curFileTypeOrIndex < af.file.typeTree.unity5Types.Count)
    {
        var type = af.file.typeTree.unity5Types[inf.curFileTypeOrIndex];
        var classIdField = type.GetType().GetField("classId") ?? type.GetType().GetField("m_TypeId");
        if (classIdField != null)
            return (int)classIdField.GetValue(type);
    }
    return inf.curFileTypeOrIndex;
}

bool IsTextAsset(AssetFileInfoEx inf) => GetClassId(inf) == TEXT_ASSET_ID;

byte[] BuildTextAssetRaw(string name, byte[] script)
{
    // TextAsset 직렬화: countstring m_Name + byte array m_Script (4바이트 정렬)
    var ms = new MemoryStream();
    using var bw = new BinaryWriter(ms);
    byte[] nb = System.Text.Encoding.UTF8.GetBytes(name);
    bw.Write(nb.Length); bw.Write(nb);
    int p1 = (4 - nb.Length % 4) % 4; bw.Write(new byte[p1]);
    bw.Write(script.Length); bw.Write(script);
    int p2 = (4 - script.Length % 4) % 4; bw.Write(new byte[p2]);
    return ms.ToArray();
}

switch (cmd)
{
    case "probe":
    {
        int i = 0;
        foreach (var inf in infos)
        {
            Console.WriteLine($"PathId={inf.index} TypeIdOrIndex={inf.curFileTypeOrIndex} ClassId={GetClassId(inf)} ScriptTypeIndex={inf.scriptIndex} Size={inf.curFileSize}");
            if (++i >= 15) break;
        }
        Console.WriteLine($"총 에셋: {infos.Length}");
        return 0;
    }
    case "types":
    {
        var counts = new Dictionary<int, int>();
        foreach (var inf in infos)
            counts[GetClassId(inf)] = counts.GetValueOrDefault(GetClassId(inf)) + 1;
        foreach (var kv in counts.OrderByDescending(kv => kv.Value))
        {
            string name = Enum.IsDefined(typeof(AssetClassID), kv.Key) ? ((AssetClassID)kv.Key).ToString() : "?";
            Console.WriteLine($"{kv.Value}\t{kv.Key}\t{name}");
        }
        return 0;
    }
    case "list":
    {
        foreach (var inf in infos)
        {
            if (!IsTextAsset(inf)) continue;
            var ti = am.GetTypeInstance(af, inf, true);
            var bf = ti.GetBaseField(1);
            string name = bf.Get("m_Name").GetValue().AsString();
            long size = bf.Get("m_Script").GetValue().AsByteArray().data.LongLength;
            Console.WriteLine($"{inf.index}\t{size}\t{name}");
        }
        return 0;
    }
    case "dump":
    {
        if (args.Length < 3) { Console.Error.WriteLine("dump는 이름 필요"); return 1; }
        string name = args[2];
        foreach (var inf in infos)
        {
            if (!IsTextAsset(inf)) continue;
            var ti = am.GetTypeInstance(af, inf, true);
            var bf = ti.GetBaseField(1);
            if (bf.Get("m_Name").GetValue().AsString() != name) continue;
            byte[] data = bf.Get("m_Script").GetValue().AsByteArray().data;
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
    case "apply":
    {
        if (args.Length < 3) { Console.Error.WriteLine("apply는 plan.json 필요"); return 1; }
        string planPath = Path.GetFullPath(args[2]);
        string outPath = args.Length >= 4 ? Path.GetFullPath(args[3]) : assetsPath;

        using var planDoc = JsonDocument.Parse(File.ReadAllText(planPath));
        var textAssets = planDoc.RootElement.GetProperty("textassets");

        var replacers = new List<AssetsReplacer>();
        int applied = 0;
        foreach (var inf in infos)
        {
            if (!IsTextAsset(inf)) continue;
            var ti = am.GetTypeInstance(af, inf, true);
            var bf = ti.GetBaseField(1);
            string name = bf.Get("m_Name").GetValue().AsString();
            if (name == null || !textAssets.TryGetProperty(name, out var prop)) continue;

            byte[] script = Convert.FromBase64String(prop.GetString() ?? "");
            byte[] raw = BuildTextAssetRaw(name, script);
            replacers.Add(new AssetsReplacerFromMemory(0, inf.index, TEXT_ASSET_ID, inf.scriptIndex, raw));
            applied++;
        }
        if (applied == 0)
        {
            Console.Error.WriteLine("plan과 일치하는 TextAsset 없음");
            return 1;
        }

        var writer = new AssetsFileWriter(outPath);
        af.file.Write(writer, 0, replacers, 0, null);
        writer.Flush();
        Console.WriteLine($"{applied}개 TextAsset 교체 → {outPath}");
        return 0;
    }
    default:
        Console.Error.WriteLine("알 수 없는 명령: " + cmd);
        return 1;
}
