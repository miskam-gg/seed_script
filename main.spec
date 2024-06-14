# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GUI\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\coord\\\\convert_coordinates.py', 'coord'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\coord\\\\coord.py', 'coord'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\count\\\\player_count_inv.py', 'count'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\count\\\\player_count_main.py', 'count'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\count\\\\player_count_mod.py', 'count'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\GUI\\\\bolt.mp3', 'GUI'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\GUI\\\\config.txt', 'GUI'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\GUI\\\\main.py', 'GUI'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\GUI\\\\RFS.png', 'GUI'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\GUI\\\\seed_config.json', 'GUI'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\tools\\\\search_squadgame.py', 'tools'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\tools\\\\shutdown.py', 'tools'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\tools\\\\start_seed_script.py', 'tools'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\tools\\\\switch_layout.py', 'tools'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\api.txt', '.'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\first_script.py', '.'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\master.py', '.'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\parameters.txt', '.'), ('C:\\\\Users\\\\Max\\\\PycharmProjects\\\\script_squad\\\\to_exe.txt', '.')],
    hiddenimports=['pyautogui'],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Max\\PycharmProjects\\script_squad\\GUI\\RFS.png'],
)
