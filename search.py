#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

delta_margin=1025

class Search:
    def __init__(self):
        # Define defualt variables during class construction.
        self.nodes=0
        self.tt_score={}
        self.tt_move={}

    def preform(self,pos):
        self.nodes=0
        # Reset the transposition table score to prevent search instabilities.
        self.tt_score={}
        best_move=()
        # Increase the depth as we go so search with 1 depth set then 2 then 3 and so on.
        # This will help the engine preform better move ordering as the depth increases.
        for depth in range(1,1000):
            best=alpha=-infinity
            beta=-alpha
            # Sort through the moves.
            for move in self.sorted(pos):
                score=-self.search(pos.move(move),-beta,-alpha,depth-1,1)
                # Preform AB Pruning.
                if score>=beta:
                    best_move=move
                    best=score
                    break
                # If the position is better than the previous one set.
                if score>best:
                    best_move=move
                    best=score
                    # Set alpha to the best score if it is outside the bounds.
                    alpha=max(alpha,score)
            # Yield the best move.
            yield best_move,depth,best

    def search(self,pos,alpha,beta,depth=3,ply=1):
        self.nodes+=1
        # Detect mate.
        if pos.dead(): return mate-ply
        # Preform Mate-Distance Pruning.
        mating_value=mate-ply;
        if mating_value<beta:
            beta=mating_value
            if alpha>=mating_value: return mating_value
        mated_value=-mate+ply;
        if mated_value>alpha:
            alpha=mated_value
            if beta<=mated_value: return mated_value
        # Prevent negitave depths in the transposition table.
        depth=max(depth,0)
        # Check to see if we have visited this position before.
        entry=self.tt_score.get(pos.hash())
        if entry and entry[1]>=depth:
            if entry[0]==0: return entry[2]
            elif entry[0]==-1: alpha=max(alpha,entry[2])
            elif entry[1]==1: beta=min(beta,entry[2])
            if alpha>=beta: return entry[2]
        # We have reached depth 0. Preform a QSearch.
        if depth==0: return self.qsearch(pos,alpha,beta,ply+1)
        # We are saving the original alpha score for transposition construction.
        o_alpha=alpha
        best=-infinity
        # Sort through the moves.
        for move in self.sorted(pos):
            # We are increamenting the ply to determine how far we went into the search.
            # This is will be used to prune the mate distance allowing the engine to go for the fastest 
            # way to mate and the longest way to be mated.
            # How? We simply return the mate score - ply.
            score=-self.search(pos.move(move),-beta,-alpha,depth-1,ply+1)
            if score>=beta:
                # This is the best move.
                # Save this move in the killers table for future searches.
                self.tt_move[pos.hash()]=move
                best=score
                break
            if score>best:
                # This is the best move.
                # Save this move in the killers table for future searches.
                self.tt_move[pos.hash()]=move
                best=score
                alpha=max(alpha,score)
        # If the best score is less than or equal to the original alpha then the position is UPPERBOUND.
        # If the best score is greater than or equal to the beta then the position is LOWERBOUND.
        # Else this position is EXACT.
        if best<=o_alpha: self.tt_score[pos.hash()]=(1,depth,best)
        elif best>=beta: self.tt_score[pos.hash()]=(-1,depth,best)
        else: self.tt_score[pos.hash()]=(0,depth,best)
        # Now we return the best score.
        return best
        
    def qsearch(self,pos,alpha,beta,ply):
        self.nodes+=1
        # Detect mate.
        if pos.dead(): return mate-ply
        # Get the current eval score.
        score=pos.score
        # Preform AB Pruning.
        if score>=beta: return beta
        # Preform Delta Pruning.
        if score<alpha-delta_margin: return alpha
        alpha=max(alpha,score)
        # Sort through the moves.
        for move in self.sorted(pos):
            # Only allow capture moves.
            if pos.board[move[1]]==0: continue
            # The search is the same, but only for capture moves.
            score=-self.qsearch(pos.move(move),-beta,-alpha,ply+1)
            # Preform AB Pruning.
            if score>=beta: return beta
            if score>alpha: alpha=score
        # Return the best score.
        return alpha

    def sorted(self,pos):
        # First we check the killer table to see if have searched this position before
        # and have determined a best move. When we search we save the best move in the killer table
        # so the next time the engines searches for the best move we search the best moves from the
        # previous search to allow for more AB pruning to take place.
        killer=self.tt_move.get(pos.hash())
        # If a killer was found yield that move first.
        if killer: yield killer
        # Now sort the moves by value of the move/
        # So for example we should be looking at captures/pawn promotions.
        for move in sorted(pos.gen_moves(),key=pos.value,reverse=True):
            # If this move matches the killer then continue, we have already yielded the killer move.
            if move==killer: continue
            yield move
