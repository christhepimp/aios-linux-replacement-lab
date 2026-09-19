# Rooted Android / Linux lab

## Path A — QEMU Linux guest (do this first)

```bash
# Debian example
sudo apt install qemu-system-x86 qemu-utils
# boot any cloud image with cloud-init or a live ISO
```

You get real root, a real kernel you can rebuild, and no Android zygote in the way.
When AetherOS init works here, *then* port ideas to Android.

## Path B — Android Studio AVD (userdebug + root)

1. Install Android Studio / cmdline-tools.
2. Create an AVD with a **Google APIs** or **AOSP** system image, not a locked production image if you can avoid it.
3. Prefer `userdebug` builds when available — `adb root` works.
4. For Play Store images, look at Emuroot (QEMU gdb patch of creds) or a custom kernel with KernelSU.

Boot with a custom kernel once you can build one:

```bash
emulator -avd YourAvd -kernel /path/to/Image.gz -show-kernel -verbose
```

Goldfish/ranchu kernel trees live under AOSP (`kernel/goldfish`, common-android*).

## Path C — Waydroid on a Linux desktop

Near-native Android apps. Shares the **host** kernel. Good for Android userspace experiments, bad as the place you “replace Linux.”

## Path D — Phone AVF / pKVM

On supported Pixels, Android can boot a real Linux VM (Debian Terminal / UserLAnd VM backend / research crosvm). That is a guest kernel. Still not “replace Android’s kernel from an app.”

## What “get in the Linux code” actually is

| You want | You open |
| --- | --- |
| Android userspace | AOSP `system/core`, `frameworks/base` |
| Android kernel | `common-android*` / device kernel |
| Emulator hypervisor | QEMU + goldfish drivers |
| Init | `system/core/init` (Android) or systemd/openrc |
| Root tooling | KernelSU, Magisk (devices), `adb root` (emulator) |

Start reading: process creation, binder, and init `.rc` files. That is the surface an AI OS would take over first.
