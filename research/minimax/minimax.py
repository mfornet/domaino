# Fast minimax game agnostic implementation
#
# * Alphabeta prunning
# * Memoization

class Minimax:
    """
    Value of each state is calculated lazy.
    It is only calculated using while alpha < beta.

    game must implement
        * first_state() -> state
        * is_max_turn(state) -> bool
        * is_over(state) -> bool
        * get_value(state) -> int (only for terminal states)
        * next_move(state, cur_position) -> (move, new_state, new_position)
    """
    def __init__(self, game):
        self.game = game
        # Map: state -> (cur_value, cur_position, best_moves)
        self.memo = dict()

    def update_ab(self, value, alpha, beta, state):
        if self.game.is_max_turn(state):
            alpha = max(alpha, value)
        else:
            beta = min(beta, value)
        return alpha, beta

    def update_value(self, cur_value, new_value, state, move, best_moves):
        if cur_value is None:
            # Always accept first value
            update = True
        else:
            if cur_value == new_value:
                # This move is as strong as previous stored move
                best_moves.append(move)
                return cur_value

            update = False
            if self.game.is_max_turn(state):
                if new_value > cur_value:
                    update = True
            else:
                if new_value < cur_value:
                    update = True

        if update:
            best_moves.clear()
            best_moves.append(move)
            return new_value
        else:
            return cur_value

    def show(self, state):
        mask, *args = state
        # print("%10s"%bin(mask), state, self.memo[state])

    def find(self, state, alpha=float('-inf'), beta=float('+inf')):
        cur_value, cur_position, best_moves = self.memo.get(state, (None, 0, []))

        if cur_position is None:
            # This state was completely explored already
            return cur_value

        if self.game.is_over(state):
            # Game is over
            # Compute current value ...
            value = self.game.get_value(state)
            # ... and memoize it
            self.memo[state] = (value, None, [])
            self.show(state)
            return value

        # Update values of alpha/beta
        if cur_value is not None:
            alpha, beta = self.update_ab(cur_value, alpha, beta, state)

        if alpha >= beta:
            # Current information is enough to know who will win through this branch
            return cur_value

        while cur_position is not None:
            (move, new_state, new_position) = self.game.next_move(state, cur_position)
            new_value = self.find(new_state, alpha, beta)
            cur_value = self.update_value(cur_value, new_value, state, move, best_moves)
            alpha, beta = self.update_ab(cur_value, alpha, beta, state)

            if alpha >= beta:
                # It is safe to finish here
                self.memo[state] = (cur_value, new_position, best_moves)
                self.show(state)
                return cur_value

            cur_position = new_position

        # All moves were explored
        self.memo[state] = (cur_value, None, best_moves)
        self.show(state)
        return cur_value

    def get_moves(self, state):
        self.find(state)
        return self.memo[state][2]