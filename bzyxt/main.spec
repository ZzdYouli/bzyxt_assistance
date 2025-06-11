# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('tools/adb.exe', 'tools'), ('tools/AdbWinApi.dll', 'tools'), ('tools/AdbWinUsbApi.dll', 'tools')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='暴走英雄坛躺床辅助器测试版v0.35',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=['AdbWinApi.dll', 'AdbWinUsbApi.dll'],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=['AdbWinApi.dll', 'AdbWinUsbApi.dll'],
    name='暴走英雄坛躺床辅助器测试版v0.35'
)
