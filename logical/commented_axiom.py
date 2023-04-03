#This is a commented axiom, like a normal axiom, but with a comment attached.

#Really this is just a holder for the axiom and the comment, which are both separate objects,
    #so that they can both stay together and it can be not annoying to translate them.

from macleod.logical.logical import Logical
from macleod.logical.axiom import Axiom
from macleod.logical.comment import Comment

class Commented_Axiom():
    def __init__(self, axiom=None, comment=None):
        if(isinstance(axiom, Logical)):
            self.axiom = Axiom(axiom)
        if(isinstance(comment, str)):
            self.comment = Comment(comment)

    def __repr__(self) -> str:
        return str(self.axiom) + " " + self.comment.text


    def to_tptp(self):
        return self.axiom.to_tptp() + " " + self.comment.to_tptp()
    
    def to_ladr(self):
        return self.axiom.to_ladr() + " " + self.comment.to_ladr()
    
    def to_latex(self):
        return self.axiom.to_latex() + " " + self.comment.to_latex()
    
    def ff_pcnf(self):
        return str(self.axiom.ff_pcnf()) + " " + self.comment.ff_pcnf()
