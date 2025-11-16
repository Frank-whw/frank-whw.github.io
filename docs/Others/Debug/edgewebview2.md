# 重装 x64 版 EdgeWebView2 的心酸

**问题背景**

- 在 `vibe coding` 开发 Dayflow（Tauri + React + Rust）时，执行 `npm run tauri dev` 报错，无法弹出原生窗口。
- 初步判断为 WebView2 运行时架构不匹配：本机需要 x64 版 Edge WebView2 Runtime。

**现象与初始尝试**

- 从 `https://developer.microsoft.com/en-us/microsoft-edge/webview` 下载 Evergreen Bootstrapper，预期自动安装匹配架构的运行时（x64）。
- 实际安装报错并失败：

![](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202511161124360.png)

- 继续尝试以管理员身份强制安装，但在对应目录未发现预期文件。

**原因分析**

- 机器上已有 32 位 WebView2，且 Evergreen 安装器存在历史行为导致目录与架构混淆：
- 官方反馈中提到 Bootstrapper/Standalone Installer 会把 x64 与 x86 都安装到 `%ProgramFiles(x86)%\Microsoft\EdgeWebView\Application` 下，后安装的版本可能覆盖前一个版本，造成异常。
- 参考：MicrosoftEdge/WebView2Feedback 的 Issue #1044：`https://github.com/MicrosoftEdge/WebView2Feedback/issues/1044`

![](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202511161127210.png)

- 验证架构可以通过查看 `msedgewebview2.exe` 的 PE 头：`8664` 为 x64，`14C` 为 x86。

**解决路径**

- 放弃 Bootstrapper，改用 Fixed Version（固定版本）运行时，避免目录和注册表的混淆。
- 下载 `.cab` 固定版本包，手动解压到自定义目录，并用环境变量指向该目录：
  - `WEBVIEW2_BROWSER_EXECUTABLE_FOLDER` 指向包含 `msedgewebview2.exe` 的解压目录
  - 可选：`WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS="--disable-gpu --enable-logging --v=1"` 用于禁用 GPU 并打开日志，排除显卡驱动问题

**固定版本安装与配置脚本（PowerShell）**

```powershell
$cabPath = "...\Microsoft.WebView2.FixedVersionRuntime.142.0.3595.80.x64.cab"
$version = "142.0.3595.80"
$destRoot = "C:\WebView2Fixed\x64"
$dest = Join-Path $destRoot $version

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Write-Host "解压到: $dest"
& expand.exe $cabPath -F:* $dest

$exe = Get-ChildItem -Path $dest -Filter msedgewebview2.exe -Recurse | Select-Object -First 1
if (-not $exe) { Write-Error "解压后未找到 msedgewebview2.exe"; exit 1 }

$env:WEBVIEW2_BROWSER_EXECUTABLE_FOLDER = (Split-Path -Parent $exe.FullName)
$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS = "--disable-gpu --enable-logging --v=1"
Write-Host "WEBVIEW2_BROWSER_EXECUTABLE_FOLDER=$env:WEBVIEW2_BROWSER_EXECUTABLE_FOLDER"
```

**结果**

- 固定版本的 WebView2 运行时已成功解压并可用。
- 通过环境变量显式指定运行时目录，可稳定为 x64 应用提供正确的 WebView2 依赖。