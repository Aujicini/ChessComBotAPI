class Search:
    def __init__(self):
        self.nodes=0
        self.tt_score={}
        self.tt_move={}

    def preform(self,pos):
        self.nodes=0
        self.tt_score={}
        best_move=()
        for depth in range(1,1000):
            best=alpha=-infinity
            beta=-alpha
            for move in self.sorted(pos):
                score=-self.search(pos.move(move),-beta,-alpha,depth-1,1)
                if score>=beta:
                    best_move=move
                    best=score
                    break
                if score>best:
                    best_move=move
                    best=score
                    alpha=max(alpha,score)
            yield best_move,depth,best

    def search(self,pos,alpha,beta,depth=3,ply=1):
        self.nodes+=1
        if pos.dead(): return mate-ply
        mating_value=mate-ply;
        if mating_value<beta:
            beta=mating_value
            if alpha>=mating_value: return mating_value
        mated_value=-mate+ply;
        if mated_value>alpha:
            alpha=mated_value
            if beta<=mated_value: return mated_value
        depth=max(depth,0)
        entry=self.tt_score.get(pos.hash())
        if entry and entry[1]>=depth:
            if entry[0]==0: return entry[2]
            elif entry[0]==-1: alpha=max(alpha,entry[2])
            elif entry[1]==1: beta=min(beta,entry[2])
            if alpha>=beta: return entry[2]
        if depth==0: return self.qsearch(pos,alpha,beta,ply+1)
        o_alpha=alpha
        best=-infinity
        for move in self.sorted(pos):
            score=-self.search(pos.move(move),-beta,-alpha,depth-1,ply+1)
            if score>=beta:
                self.tt_move[pos.hash()]=move
                best=score
                break
            if score>best:
                self.tt_move[pos.hash()]=move
                best=score
                alpha=max(alpha,score)
        if best<=o_alpha: self.tt_score[pos.hash()]=(1,depth,best)
        elif best>=beta: self.tt_score[pos.hash()]=(-1,depth,best)
        else: self.tt_score[pos.hash()]=(0,depth,best)
        return best
        
    def qsearch(self,pos,alpha,beta,ply):
        self.nodes+=1
        if pos.dead(): return mate-ply
        score=pos.score
        if score>=beta: return beta
        if score<alpha-delta_margin: return alpha
        alpha=max(alpha,score)
        for move in self.sorted(pos):
            if pos.board[move[1]]==0: continue
            score=-self.qsearch(pos.move(move),-beta,-alpha,ply+1)
            if score>=beta: return beta
            if score>alpha: alpha=score
        return alpha

    def sorted(self,pos):
        killer=self.tt_move.get(pos.hash())
        if killer: yield killer
        for move in sorted(pos.gen_moves(),key=pos.value,reverse=True): 
            if move==killer: continue
            yield move
