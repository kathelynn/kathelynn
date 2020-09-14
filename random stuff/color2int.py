print("""
# # # # # # # # # # # # # #
# color2int:              #
# 1. RGB Values > Integer #
# 2. Integer > RGB Values #
# Or press Enter to Quit  #
# # # # # # # # # # # # # #"""
)
mode = input('> ')
if mode == '1':
    R = int(input('R: '))
    G = int(input('G: '))
    B = int(input('B: '))
    print((R << 16) + (G << 8) + B)
if mode == '2':
    C = int(input('Integer: '))
    print(f'R: {(C >> 16) & 255} G: {(C >> 8) & 255} B: {C & 255}')