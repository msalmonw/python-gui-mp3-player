# python-gui-mp3-player
Python program that can play mp3 files with interactive GUI

Features: 

1) Make a playlist by browsing to a folder containing mp3 files
2) Pause/play music (keyboard: spacebar)
2) Go to next or previous song in the playlist (keyboard: p/n)
3) Skip forwards or backwards (keyboard: ctrl + right-arrow/left-arrow(60 seconds), right/left-arrow(10 seconds))
4) Change volume (keyboard: up/down-arrow)

Known Issues: 

1) Even if a single mp3 file's metadata is empty in a folder, none of the files can be played. For now you can manually add the titles of
   such mp3 files to their metadata to resolve this issue.
2) Clicking anywhere on the duration bar during playback will cause issues with the playback. Jump to next/previous song to as a workaround.
