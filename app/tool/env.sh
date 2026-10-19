# Muat toolchain Makhraj untuk sesi Git Bash ini saja.
# Pakai:  source tool/env.sh
export FLUTTER_ROOT="/d/dev/flutter"
export JAVA_HOME="$(ls -d /d/dev/jdk-17* | head -1)"
export ANDROID_HOME="/d/dev/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PUB_CACHE="D:\\dev\\pub-cache"
export GRADLE_USER_HOME="D:\\dev\\gradle"
export PATH="$FLUTTER_ROOT/bin:$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"
