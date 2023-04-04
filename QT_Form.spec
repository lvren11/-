# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['QT_Form.py','parameters.py','Parameter_ui.py','save_tool.py','Worker.py','program.py','func.py','QT_MAINUI.py','Tooltip_ui.py','progress.py','logo.py','add_address.py','add_user.py','login.py','update_pwd.py','User_manage.py','update_admin.py'
],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='QT_Form',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='logo.ico')
