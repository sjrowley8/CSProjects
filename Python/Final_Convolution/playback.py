GAME = 'ppd/pixel_batch_1.pkl'

import pickle

boards, moves = pickle.load(open(GAME, 'rb'))

print(boards[0])

