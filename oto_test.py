from configparser import ConfigParser
from collections import namedtuple
from types import MappingProxyType
from typing import Iterable, Optional

pitch = [f'{letter}{number}'
         for number in '1234567'
         for letter in 'C C# D D# E F F# G G# A A# B'.split(' ')]

Pitch = MappingProxyType({key: value for key, value in zip(pitch, range(24, 108))})


class Note(namedtuple('Note', 'Length Lyric NoteNum')):
    """storing basic note information by using namedtuple

    Args:
        namedtuple ([type]): note length, lyric and the number representing the pitch
    """
    def __str__(self) -> str:
        return f'[#0000]\nLength={self.Length}\nLyric={self.Lyric}\nNoteNum={self.NoteNum}'
    
class OTO_Test:
    EmptyNote = Note(480, 'R', 60)
    vowel: list[str] = []
    consonant: tuple[str, ...]
    vowel_dict: dict[str, list[str]] = {}
    consonant_dict: dict[str, list[str]] = {}
    note_list: list[Note] = []
    
    def read_presamp(self, presamp_dir: str) -> None:
        """read presamp.ini

        Args:
            presamp_dir ([str]): the path of presamp.ini file.
        """
        presamp = ConfigParser(allow_no_value=True)
        presamp.read(presamp_dir)
        for vowel, cvs in presamp['VOWEL'].items():
            cv_union = [cv for cv in cvs.split('=')[1].split(',')]
            self.vowel_dict[vowel] = cv_union
            self.vowel.append(vowel)
        for consonant, cvs in presamp['CONSONANT'].items():
            cv_union = [cv for cv in cvs.split('=')[0].split(',')]
            self.consonant_dict[consonant] = cv_union
        
    def find_cv(self, c: str=None, v: str=None) -> str:
        """use consonant or vowel to find cv.

        Args:
            c (str, optional): consonant. Defaults to None.
            v (str, optional): vowel. Defaults to None.

        Raises:
            TypeError: given wrong type, neither c or v

        Returns:
            str: cv
        """
        if c:
            return self.consonant_dict[c][0]
        elif v:
            return self.vowel_dict[v][0]
        else:
            raise TypeError
        
        
    def test_consonant(self, consonant: Iterable[str], pitch: str) -> None:
        """test vc components like smoothness.

        Args:
            consonant (Iterable[str]): [description]
            pitch (str): [description]
        """
        cv = [self.find_cv(c=c) for c in consonant]
        v = [self.find_cv(v=v) for v in self.vowel]
        
        cv_note_union = [Note(480, lyric, Pitch[pitch]) for lyric in cv]
        v_note_union = [Note(480, lyric, Pitch[pitch]) for lyric in v]
            
        self.note_list.clear()
        self.note_list.append(self.EmptyNote)
        for cv_note in cv_note_union:
            for v_note in v_note_union:
                self.note_list.extend((v_note, cv_note, self.EmptyNote))
                
    def test_vv(self, pitch: str, vowel: Optional[Iterable[str]]=None) -> None:
        """test vv components like pre line accuracy.

        Args:
            pitch (str): pitch sign like C4
            vowel (Optional[Iterable[str]], optional): 
                if leave it to default, mean all vv components are added. 
                Defaults to None.

        Raises:
            SyntaxError: Given vowel cannot form vv accroding to presamp file.
        """
        v1 = [self.find_cv(v=v) for v in self.vowel]
        if vowel is None:
            v2 = [v for v in self.vowel if v in self.find_cv(v=v) in self.vowel]
        else:
            v2 = []
            for v in vowel:
                if  (v := self.find_cv(v=v)) in self.vowel:
                    v2.append(v)
                else:
                    raise SyntaxError(f'Given vowel: {v} cannot form vv accroding to presamp file.')
        
        v1_note_union = [Note(480, lyric, Pitch[pitch]) for lyric in v1]
        v2_note_union = [Note(480, lyric, Pitch[pitch]) for lyric in v2]
        self.note_list.clear()
        self.note_list.extend((self.EmptyNote, self.EmptyNote))
        for v2 in v2_note_union:
            for v1 in v1_note_union:
                self.note_list.extend((v1, v2, self.EmptyNote, self.EmptyNote))
                self.note_list.extend((v1, v2, self.EmptyNote, self.EmptyNote))
        
    def save_ust(self, ust_dir: str='result.ust') -> None:
        """save ust file. 
        
        Args:
            ust_dir (str, optional): ust file path. Defaults to 'result.ust'.
        """
        with open(ust_dir, mode='w', encoding='shift-jis') as ust_file:
            ust_file.write('\n'.join(str(note) for note in self.note_list))
            
            
def main():
    test = OTO_Test()
    test.read_presamp('presampCHN.ini')
    test.test_consonant(('z', 'zh', 'j', 'q', 'c', 'ch'), 'A3')
    test.save_ust('vc_test.ust')
    test.test_vv('A3')
    test.save_ust('vv_test.ust')
    

if __name__ == '__main__':
    main()