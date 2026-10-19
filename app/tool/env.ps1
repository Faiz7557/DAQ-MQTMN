# Muat toolchain Makhraj untuk sesi PowerShell ini saja (tidak mengubah pengaturan sistem).
# Pakai:  . .\tool\env.ps1
$dev = "D:\dev"
$env:FLUTTER_ROOT = "$dev\flutter"
$env:JAVA_HOME = (Get-ChildItem $dev -Directory -Filter "jdk-17*" | Select-Object -First 1).FullName
$env:ANDROID_HOME = "$dev\android-sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:PUB_CACHE = "$dev\pub-cache"
$env:GRADLE_USER_HOME = "$dev\gradle"
# Flutter memanggil `where` dan `git`, jadi System32 dan folder git harus ada di PATH.
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
$gitDir = if ($gitCmd) { Split-Path $gitCmd.Source } else { "C:\laragon\bin\git\bin" }
$sys = "$env:SystemRoot\System32;$env:SystemRoot;$env:SystemRoot\System32\WindowsPowerShell\v1.0"
$env:Path = "$env:FLUTTER_ROOT\bin;$env:JAVA_HOME\bin;$env:ANDROID_HOME\cmdline-tools\latest\bin;$env:ANDROID_HOME\platform-tools;$gitDir;$sys;$env:Path"
