#This is a commented axiom, like a normal axiom, but with a comment attached.

#Really this is just a holder for the axiom and the comment, which are both separate objects,
    #so that they can both stay together and it can be not annoying to translate them.

class Commented_Axiom():
    def __init__(self, axiom=None, comment=None):
        self.axiom = axiom
        self.comment = comment


    def to_tptp(self):
        return self.axiom.to_tptp() + self.comment.to_tptp()
    
    def to_ladr(self):
        return self.axiom.to_ladr() + self.comment.to_ladr()
    
    def to_latex(self):
        return self.axiom.to_latex() + self.comment.to_latex()
