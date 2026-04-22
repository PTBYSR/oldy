[Setup]
AppName=Oldy
AppVersion=0.1.0
DefaultDirName={localappdata}\Programs\Oldy
DefaultGroupName=Oldy
OutputDir=dist
OutputBaseFilename=OldySetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
ChangesEnvironment=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\oldy.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
