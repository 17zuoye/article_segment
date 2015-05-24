# -*- coding: utf-8 -*-

import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import unittest
from article_segment import article_segment


class TestFillBrokenWords(unittest.TestCase):

    def test_(self):
        assert article_segment("       u se    c u te  ") == "       use cute"
        assert article_segment("fl y       k i te  ") == "fly kite"
        assert article_segment("k i te   l i ve") == "kite live"
        assert article_segment("ea r   h ea d") == "ear head"
        assert article_segment(" f ir st   th ir d         ") == " first third"
        assert article_segment("s o     o n ") == "soon"

        assert article_segment("A. s un  B.no s e C.fa c e  D.ri c e", True) == "A. sun B. nose C. face D. rice"
        assert article_segment(" A.j u mp       B.st u dy      C.J u ly", True) == " A. jump B. study C. July"

        # copied from http://en.wikipedia.org/wiki/Peter_Norvig
        long_txt = article_segment("""He is a Fellow and Councilor of the Association for the Advancement of Artificial Intelligence and co-author, with Stuart Russell, of Artificial Intelligence: A Modern Approach, now the leading college text in the field[citation needed]. He previously was head of the Computational Sciences Division (now the Intelligent Systems Division) at NASA Ames Research Center, where he oversaw a staff of 200 scientists performing NASA's research and development in autonomy and robotics, automated software engineering and data analysis, neuroengineering, collaborative systems research, and simulation-based decision-making. Before that he was Chief Scientist at Junglee, where he helped develop one of the first Internet comparison shopping services; Chief designer at Harlequin Inc.; and Senior Scientist at Sun Microsystems Laboratories. " +
                A.j u mp       B.st u dy      C.J u ly
                Norvig received a Bachelor of Science in Applied Mathematics from Brown University[6] and a Ph.D. in Computer Science from the University of California, Berkeley.""",)

        assert " A. jump B. study C. July" in long_txt


if __name__ == '__main__':
    unittest.main()
