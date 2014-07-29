# -*- coding: utf-8 -*-

# TODO 切分300个长度以上的字符组。
# TODO 切分错误就撤销回去

# load unigrams and bigrams texts.
import re
import os
import sys

from etl_utils import cached_property, singleton
from split_block import SplitBlockGroup, SplitBlock

@singleton()
class ArticleSegment(object):
    def load_grams(self):
        cache_dir = None
        try:
            from wordsegment import segment
        except IOError, e:
            cache_dir = os.path.dirname(e.filename)

        if cache_dir: # if there's none grams texts
            grams_urls = ["https://github.com/mvj3/wordsegment/blob/master/unigrams.txt",
                          "https://github.com/mvj3/wordsegment/blob/master/bigrams.txt",]

            for url1 in grams_urls:
                grams_path = os.path.join(cache_dir, url1.split("/")[-1])
                os.system("wget %s %s/" % (url1, cache_dir))

    @cached_property
    def segment(self):
        self.load_grams()
        from wordsegment import segment
        return segment

    def isupper(self, str1, idx1=0):
        if len(str1) < (idx1+1): return False
        return str1[idx1].isupper()

    def fix_blanks(self, split_block_group, item1, idx1, offset):
        if offset not in [1, -1]: raise NotImplemented
        if (offset == -1) and (idx1 == 0): return False

        item2 = split_block_group[idx1 + offset]
        if (isinstance(item2, SplitBlock) and (not item2.is_blank)):
            item1 = (item1 + ' ') if offset is 1 else (' ' + item1)
            split_block_group[idx1] = item1


    def article_segment(self, sentence, inspect=False):
        sentence = re.sub("\xc2\xa0", " ", sentence)

        split_block_group = SplitBlockGroup.extract(sentence)
        index_block__to__fixed_words = dict()

        # Generate fixed words and their indexes.
        for chapped_group1 in split_block_group.maybe_chapped_groups():
            chapped_group1 = SplitBlockGroup(chapped_group1)

            # Reject upper words
            # Iterate to remove continuous upper items
            rejected_items = set([])
            letters = chapped_group1.letters()
            for idx1, letter1 in enumerate(letters):
                if (idx1 + 1) == len(letters): break
                if inspect: print letters
                if self.isupper(letter1.string) and self.isupper(letters[idx1+1].string, 1):
                    rejected_items.add(letter1)
                    rejected_items.add(letters[idx1+1])
            for rejected_item1 in rejected_items:
                chapped_group1.remove(rejected_item1)

            chapped_strs   = "".join(chapped_group1.concat_items().split(" "))
            fixed_words    = " ".join(self.segment(chapped_strs))
            if inspect: print fixed_words

            index_block__to__fixed_words[(chapped_group1[0].pos_begin, chapped_group1[-1].pos_end,)] = fixed_words
        if inspect:
            print
            print "[split_block_group.maybe_chapped_groups()]", split_block_group.maybe_chapped_groups()
            print "[index_block__to__fixed_words]", index_block__to__fixed_words
            print "\n"*5

        # Fill fixed words by their indexes.
        for begin_end_pos in index_block__to__fixed_words:
            begin_idx1, end_idx1 = None, None
            for idx2, sb2 in enumerate(split_block_group):
                if isinstance(sb2, str): continue
                if begin_end_pos[0] == sb2.pos_begin: begin_idx1 = idx2
                if begin_end_pos[1] == sb2.pos_end:   end_idx1   = idx2
            split_block_group[begin_idx1:end_idx1+1] = index_block__to__fixed_words[begin_end_pos]
            if inspect: print split_block_group; print

        # Fix blanks
        for idx1, item1 in enumerate(split_block_group[:]):
            if not isinstance(item1, str): continue
            if (idx1 + 1) == len(split_block_group) - 1: break

            self.fix_blanks(split_block_group, item1, idx1, 1)
            self.fix_blanks(split_block_group, item1, idx1, -1)

        if inspect: print split_block_group.concat_items(); print
        return split_block_group.concat_items()

article_segment = ArticleSegment().article_segment

"""
(Pdb) segment("sunB")
['sunB']
(Pdb) segment("sunb")
['sun', 'b']
"""
