
[app]

title = BACHARTELB PASSWORD GENERATOR PRO

package.name = bacharpassword
package.domain = org.bachar

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
icon.filename = %(source.dir)s/file_000000006edc820ea88cece3dae54ce0.png

requirements = python3,kivy,cryptography

android.archs = arm64-v8a
 
orientation = portrait
fullscreen = 0

android.permissions =

android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.sdk_tools = cmdline-tools/latest
android.api = 33
android.minapi = 21

p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1

