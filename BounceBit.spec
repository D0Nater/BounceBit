# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BounceBit.py'],
             pathex=['C:/BounceBit'],
             binaries=[],
             datas=[
               ('pictures/main_logo1.jpg', 'pictures'),
               ('pictures/program_icon.ico', 'pictures'),

               ('pictures/play_button.png', 'pictures'),
               ('pictures/pause_button.png', 'pictures'),

               ('pictures/add_button.png', 'pictures'),
               ('pictures/add_button_click.png', 'pictures'),

               ('pictures/save_button.png', 'pictures'),
               ('pictures/save_button_click.png', 'pictures'),

               ('pictures/behind_song_button.png', 'pictures'),
               ('pictures/after_song_button.png', 'pictures'),

               ('pictures/more_button.png', 'pictures'),
               ('pictures/more_music_button.png', 'pictures'),

               ('pictures/search_button.png', 'pictures'),
               ('pictures/new_playlist_button.png', 'pictures'),

               ('pictures/ok_button.png', 'pictures'),
               ('pictures/close_button.png', 'pictures'),

               ('pictures/copy_button.png', 'pictures'),
               ('pictures/trashcan_button.png', 'pictures'),

               ('pictures/edit_button.png', 'pictures'),
               ('pictures/update_button.png', 'pictures'),

               ('pictures/Light/play_button.png', 'pictures/Light'),
               ('pictures/Light/pause_button.png', 'pictures/Light'),

               ('pictures/Light/add_button.png', 'pictures/Light'),
               ('pictures/Light/add_button_click.png', 'pictures/Light'),

               ('pictures/Light/save_button.png', 'pictures/Light'),
               ('pictures/Light/save_button_click.png', 'pictures/Light'),

               ('pictures/Light/behind_song_button.png', 'pictures/Light'),
               ('pictures/Light/after_song_button.png', 'pictures/Light'),

               ('pictures/Light/more_button.png', 'pictures/Light'),
               ('pictures/Light/more_music_button.png', 'pictures/Light'),

               ('pictures/Light/search_button.png', 'pictures/Light'),
               ('pictures/Light/new_playlist_button.png', 'pictures/Light'),

               ('pictures/Light/ok_button.png', 'pictures/Light'),
               ('pictures/Light/close_button.png', 'pictures/Light'),

               ('pictures/Light/copy_button.png', 'pictures/Light'),
               ('pictures/Light/trashcan_button.png', 'pictures/Light'),

               ('pictures/Light/edit_button.png', 'pictures/Light'),
               ('pictures/Light/update_button.png', 'pictures/Light')
             ],
             hiddenimports=[],
             hookspath=[],
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
          name='BounceBit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
