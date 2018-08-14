# import cx_Freeze
# executables = [cx_Freeze.Executable("BrandonsTetris.py")]
# cx_Freeze.setup(
#     name="Tetris by Brandon Li",
#     options={"build_exe": {"packages":["pygame"],
#                            "include_files":["backround.png","backround2.png","backround3.png","/Users/BrandonLi/Documents/tetris2p/Comic-Panels.woff", "HomeButton.png", "HomeButton2.png", "Help.png", "Tetris.png", "block.png", "lightButton.png", "DarkButton.png", "fire.png", "/Users/BrandonLi/Documents/tetris2p/KOMIKAX_.woff", "backroundTop.png"]}},
#     executables = executables

#     )
x = 0
import BrandonsTetris
while True:
    x += 10
    if x < 300:
        BrandonsTetris.run(BrandonsTetris.width, BrandonsTetris.height)