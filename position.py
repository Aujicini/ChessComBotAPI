from collections import namedtuple
from itertools import count

COLORS_R=(2,3,0,1)
N,E,S,W=-16,1,16,-1
DOUBLE_PAWNS=(N,E,S,W)
CASTLE_ROOKS=(S,E,N,W)
KS_ROOKS=(36,81,206,251)
QS_ROOKS=(43,94,244,193)
KS_CASTLE=[(36,38),(206,174),(251,249),(81,113)]
QS_CASTLE=[(244,247),(193,145),(43,40),(94,142)]
CASTLER={"a8a10":81,"a8a6":193,"g14e14":36,"g14i14":43,"n7n5":206,"n7n9":94,"h1j1":251,"h1f1":244}
PIECES={"rP":(0,0),"rN":(0,4),"rB":(0,5),"rR":(0,6),"rQ":(0,7),"rK":(0,8),"bP":(1,1),"bN":(1,4),"bB":(1,5),"bR":(1,6),"bQ":(1,7),"bK":(1,8),"yP":(2,2),"yN":(2,4),"yB":(2,5),"yR":(2,6),"yQ":(2,7),"yK":(2,8),"gP":(3,3),"gN":(3,4),"gB":(3,5),"gR":(3,6),"gQ":(3,7),"gK":(3,8)}
PROMOTION=[(81,82,83,84,85,86,87,88,89,90,91,92,93,94),(43,59,75,91,107,123,139,155,171,187,203,219,235,251),(193,194,195,196,197,198,199,200,201,202,203,204,205,206),(36,52,68,84,100,116,132,148,164,180,196,212,228,244)]
PSTART=(52,53,54,55,56,57,58,59,82,98,114,130,146,162,178,194,93,109,125,141,157,173,189,205,228,229,230,231,232,233,234,235)
BLANK=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
INITIAL=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,(2,6),(2,4),(2,5),(2,8),(2,7),(2,5),(2,4),(2,6),0,0,0,0,0,0,0,0,(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),(2,2),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,(1,6),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,6),0,0,(1,4),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,4),0,0,(1,5),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,5),0,0,(1,8),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,7),0,0,(1,7),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,8),0,0,(1,5),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,5),0,0,(1,4),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,4),0,0,(1,6),(1,1),0,0,0,0,0,0,0,0,0,0,(3,3),(3,6),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),0,0,0,0,0,0,0,0,(0,6),(0,4),(0,5),(0,7),(0,8),(0,5),(0,4),(0,6),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
REVERT_CORD={"d14":36,"e14":37,"f14":38,"g14":39,"h14":40,"i14":41,"j14":42,"k14":43,"d13":52,"e13":53,"f13":54,"g13":55,"h13":56,"i13":57,"j13":58,"k13":59,"d12":68,"e12":69,"f12":70,"g12":71,"h12":72,"i12":73,"j12":74,"k12":75,"a11":81,"b11":82,"c11":83,"d11":84,"e11":85,"f11":86,"g11":87,"h11":88,"i11":89,"j11":90,"k11":91,"l11":92,"m11":93,"n11":94,"a10":97,"b10":98,"c10":99,"d10":100,"e10":101,"f10":102,"g10":103,"h10":104,"i10":105,"j10":106,"k10":107,"l10":108,"m10":109,"n10":110,"a9":113,"b9":114,"c9":115,"d9":116,"e9":117,"f9":118,"g9":119,"h9":120,"i9":121,"j9":122,"k9":123,"l9":124,"m9":125,"n9":126,"a8":129,"b8":130,"c8":131,"d8":132,"e8":133,"f8":134,"g8":135,"h8":136,"i8":137,"j8":138,"k8":139,"l8":140,"m8":141,"n8":142,"a7":145,"b7":146,"c7":147,"d7":148,"e7":149,"f7":150,"g7":151,"h7":152,"i7":153,"j7":154,"k7":155,"l7":156,"m7":157,"n7":158,"a6":161,"b6":162,"c6":163,"d6":164,"e6":165,"f6":166,"g6":167,"h6":168,"i6":169,"j6":170,"k6":171,"l6":172,"m6":173,"n6":174,"a5":177,"b5":178,"c5":179,"d5":180,"e5":181,"f5":182,"g5":183,"h5":184,"i5":185,"j5":186,"k5":187,"l5":188,"m5":189,"n5":190,"a4":193,"b4":194,"c4":195,"d4":196,"e4":197,"f4":198,"g4":199,"h4":200,"i4":201,"j4":202,"k4":203,"l4":204,"m4":205,"n4":206,"d3":212,"e3":213,"f3":214,"g3":215,"h3":216,"i3":217,"j3":218,"k3":219,"d2":228,"e2":229,"f2":230,"g2":231,"h2":232,"i2":233,"j2":234,"k2":235,"d1":244,"e1":245,"f1":246,"g1":247,"h1":248,"i1":249,"j1":250,"k1":251}
COORDINATES=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"d14","e14","f14","g14","h14","i14","j14","k14",0,0,0,0,0,0,0,0,"d13","e13","f13","g13","h13","i13","j13","k13",0,0,0,0,0,0,0,0,"d12","e12","f12","g12","h12","i12","j12","k12",0,0,0,0,0,"a11","b11","c11","d11","e11","f11","g11","h11","i11","j11","k11","l11","m11","n11",0,0,"a10","b10","c10","d10","e10","f10","g10","h10","i10","j10","k10","l10","m10","n10",0,0,"a9","b9","c9","d9","e9","f9","g9","h9","i9","j9","k9","l9","m9","n9",0,0,"a8","b8","c8","d8","e8","f8","g8","h8","i8","j8","k8","l8", "m8","n8",0,0,"a7","b7","c7","d7","e7","f7","g7","h7","i7","j7","k7","l7","m7","n7",0,0,"a6","b6","c6","d6","e6","f6","g6","h6","i6","j6","k6","l6","m6","n6",0,0,"a5","b5","c5","d5","e5","f5","g5","h5","i5","j5","k5","l5","m5","n5",0,0,"a4","b4","c4","d4","e4","f4","g4","h4","i4","j4","k4","l4","m4","n4",0,0,0,0,0,"d3","e3","f3","g3","h3","i3","j3","k3",0,0,0,0,0,0,0,0,"d2","e2","f2","g2","h2","i2","j2","k2",0,0,0,0,0,0,0,0,"d1","e1","f1","g1","h1","i1","j1","k1",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
VALID_KEYS=(36,37,38,39,40,41,42,43,52,53,54,55,56,57,58,59,68,69,70,71,72,73,74,75,81,82,83,84,85,86,87,88,89,90,91,92,93,94,97,98,99,100,101,102,103,104,105,106,107,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,129,130,131,132,133,134,135,136,137,138,139,140,141,142,145,146,147,148,149,150,151,152,153,154,155,156,157,158,161,162,163,164,165,166,167,168,169,170,171,172,173,174,177,178,179,180,181,182,183,184,185,186,187,188,189,190,193,194,195,196,197,198,199,200,201,202,203,204,205,206,212,213,214,215,216,217,218,219,228,229,230,231,232,233,234,235,244,245,246,247,248,249,250,251)
DIRECTIONS=[(N,N+N,N+E,N+W),(E,E+E,E+N,E+S),(S,S+S,S+E,S+W),(W,W+W,W+N,W+S),(N+N+W,N+N+E,E+E+N,E+E+S,W+W+N,W+W+S,S+S+W,S+S+E),(N+E,N+W,S+E,S+W),(N,S,E,W),(N,S,E,W,N+E,N+W,S+E,S+W),(N,S,E,W,N+E,N+W,S+E,S+W)]
COLORS={"R":0,"B":1,"Y":2,"G":3}

class Position(namedtuple('Position', 'board color enpassants castling')):
    def gen_moves(self,color=-1):
        ret=[]
        for key,square in enumerate(self.board):
            if square==0 or square[0]!=color: continue
            for location in DIRECTIONS[square[1]]:
                for keyr in count(key+location,location):
                    if keyr not in VALID_KEYS: break
                    elif self.board[keyr]==0: captured=False
                    elif self.board[keyr][0]==self.color or self.board[keyr][0]==COLORS_R[self.color]: break
                    else: captured=True
                    if square[1] in (0,1,2,3) and location in (N,S,E,W) and captured: break
                    if square[1] in (0,1,2,3) and location in (N+N,S+S,W+W,E+E) \
                        and (captured or (key not in PSTART or self.board[keyr-DOUBLE_PAWNS[self.color]])!=0): break
                    if square[1] in (0,1,2,3) and location in (N+E,N+W,S+E,S+W) \
                        and not captured and (key+DOUBLE_PAWNS[self.color],keyr) not in self.enpassants: break
                    if square[1] in (0,1,2,3) and keyr in PROMOTION[self.color]:
                        ret.append((key,keyr,4))
                        ret.append((key,keyr,5))
                        ret.append((key,keyr,6))
                        ret.append((key,keyr,7))
                    else: ret.append((key,keyr))
                    if square[1] in (0,1,2,3,4,8) or captured: break
                    if not captured and (key,keyr) in KS_CASTLE and self.castling[0][color]==True:
                        ret.append((keyr-CASTLE_ROOKS[color],keyr+CASTLE_ROOKS[self.color],key))
                    if not captured and (key,keyr) in QS_CASTLE and self.castling[0][color]==True:
                        ret.append((keyr+CASTLE_ROOKS[color],keyr-CASTLE_ROOKS[self.color],key))
        return ret

    def move(self,move):
        board,enpassants,castling=self.board[:],self.enpassants[:],self.castling[:]
        enpassants[self.color]=(0,0)
        if board[move[0]][1] in (0,1,2,3):
            if move[1] in PROMOTION[self.color]: board[move[0]]=(self.color,move[2])
            if abs(move[1]-move[0]) in (32,2): enpassants[self.color]=(move[1],move[1]-DOUBLE_PAWNS[self.color])
        if board[move[0]][1]==8:
            castling[0][self.color]=castling[1][self.color]=False
            if abs(move[1]-move[0]) in (32,2):
                board[(move[0]+move[1])//2]=(self.color,6)
                board[move[2]]=0
        if board[move[0]][1]==6:
            if move[0] in KS_ROOKS: castling[0][self.color]=False
            if move[0] in QS_ROOKS: castling[1][self.color]=False
        board[move[1]]=board[move[0]]
        board[move[0]]=0
        if (move[0]+DOUBLE_PAWNS[self.color],move[1]) in self.enpassants:
            board[move[0]+DOUBLE_PAWNS[self.color]]=0
        return Position(board,(self.color+1)%4,enpassants,castling)

    def load(fen):
        fen=fen.split('-')
        castling=[[False,False,False,False],[False,False,False,False]]
        pointer=0
        for castling_ks in fen[2].split(','):
            if int(castling_ks)==1: castling[0][pointer]=True
            pointer=(pointer+1)%4
        for castling_qs in fen[3].split(','):
            if int(castling_qs)==1: castling[1][pointer]=True
            pointer=(pointer+1)%4
        enpassants=[(0,0),(0,0),(0,0),(0,0)]
        if 'enPassant' in fen[6]:
            info=fen[6].split('(')
            info=info[1].strip(')\'"')
            values=info.split(',')
            for value in values:
                value=value.strip("')}")
                if value!='':
                    squares=value.split(':')
                    enpassants[pointer]=(REVERT_CORD[squares[0]],REVERT_CORD[squares[1]])
                pointer=(pointer+1)%4
            fen[6]=fen[7]
        board=BLANK[:]
        ranks=fen[6].split('/')
        for rank in ranks:
            squares=rank.split(',')
            for square in squares:
                if square in ('1','2','3','4','5','6','7','8','9','10','11','12','13','14'): pointer+=int(square)
                else:
                    board[pointer+33]=PIECES[square]
                    pointer+=1
            pointer+=2
        return Position(board,0,COLORS[fen[0]],enpassants,castling)

    def render(self):
        g=m=r=""
        a=iter(self.board[:])
        for c in range(36): next(a)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for d in range(3):
            for e in range(8):
                f=next(a)
                if f==0: g+="     |"
                else: g+=" "+str(f[0])+"."+str(f[1])+" |"
            if d<2:
                for h in range(8): next(a)
            print("|-----|-----|-----|"+g+"-----|-----|-----|\n")
            print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            g=""
        for j in range(5): next(a)
        for k in range(8):
            for l in range(14):
                t=next(a)
                if t==0: m+="     |"
                else: m+=" "+str(t[0])+"."+str(t[1])+" |"
            if k<7:
                for i in range(2): next(a)
            print("|"+m+"\n")
            print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            m=""
        for n in range(5): next(a)
        for o in range(3):
            for p in range(8):
                q=next(a)
                if q==0: r+="     |"
                else: r+=" "+str(q[0])+"."+str(q[1])+" |"
            if o<2:
                for s in range(8): next(a)
            print("|-----|-----|-----|"+r+"-----|-----|-----|\n")
            print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
            r=""
