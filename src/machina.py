INFINITY = 1000000
MATE = INFINITY - 100000

def Search:
    def __init__():
        self.nodes = 0

    def preform(self, position):
        # Since we a preforming a new search we should reset the
        # current nodes back to 0. This will keep track on how many
        # board states the engine looks at.
        self.nodes = 0
        # We should increase the search depth as we go, this will
        # improve move ordering, and allow the engine to preform better.
        for depth in range(1, 1000):
            # Call the negamax function and get the score for the
            # current position based on the requested depth.
            score = self.search(position, -INFINITY, INFINITY, depth)

    
    def search(self, position, alpha, beta, depth, ply=0, root=True, pv_node=False, cut_node=False):
        # Increment the global nodes variable to keep track of how many
        # board states have been processed.
        self.nodes += 1
        # Here we apply mate distance pruning which prunes positions
        # all the long mates and goes for the quickest mate.
        if MATE - ply < beta and not root:
            beta = MATE - ply
            if alpha >= MATE - ply: return MATE - ply
        if -MATE + ply > alpha and not root:
            alpha = -MATE + ply
            if beta <= -MATE + ply: return -MATE + ply
        # Conduct a QSearch if the depth has reached 0.
        if depth <= 0: return self.qsearch(position, alpha, beta, ply)
        # Bestmove is set to -INFINITY then it will look for
        # moves that have a higher score and update this variable.
        best = -INFINITY
        # Go through the list of avaliable.
        # Start with searching moves that have a higher move score.
        for move in sorted(position.moves(), key=position.value, reverse=True):
            # Call the negamax function again and get the score for the
            # current position based on the requested depth, but this time
            # we will state this is not the root node.
            score = -self.search(position.move(move), -beta, -alpha, depth-1, ply+1, root=False)
            # Preform the fail-soft beta cutoff to prevent a search
            # for trees we do not need to search.
            if score >= beta and not root: return score
            # If the negamax returns a score higher than best than
            # we update best with the new score. Also if the score is
            # higher than alpha then its outside the bounds so alpha will
            # equal the given score of the current move.
            if score > best:
                best = score
                if score > alpha: alpha = score
        # Now we finally return the best score
        # if this is the root node, we return the bestmove
        return best

    def qsearch(self, position, alpha, beta, ply):
        # Increment the global nodes variable to keep track of how many
        # board states have been processed.
        self.nodes += 1
        # Get the evaluation of the current position.
        if position.turn in (0,2): stand_pat = position.evaluate()
        else: stand_pat = -position.evaluate()
        # If the evaluation fails-low then there is no need to do any more
        # QSearch with this position.
        if stand_pat >= beta: return beta
        # We attempt to apply delta pruning which tests to see if alpha
        # can be improved.
        if stand_pat < alpha - PVS[7]: return alpha
        # If the evaluation fails-high then we would set alpha to evaluation
        if alpha < stand_pat: alpha = stand_pat
        # Go through the list of avaliable.
        # Start with searching moves that have a higher move score.
        for move in sorted(position.moves(), key=position.value, reverse=True):
            # Skip moves that that are not capture moves.
            if move[2] == 0: continue
            # Get the score of the position.
            score = -self.qsearch(position.move(move), -beta, -alpha)
            # Preform the fail-soft beta cutoff to prevent a search
            # for trees we do not need to search.
            if score >= beta: return beta
            # if the score is higher than alpha then its outside the bounds
            # so alpha will equal the given score of the current move.
            if score > alpha: alpha = score
        # Return alpha which is usually the best possible score.
        return alpha
