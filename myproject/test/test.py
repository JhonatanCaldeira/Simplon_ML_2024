import sys
import os

#The same of ../
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(parent_dir)

try:
    import components.mymodule
except ImportError as e:
    print("Error importing components: ", e)

from components.mymodule import my_concatenate, my_sum

class TestMyModule():

    def test_my_sum(self):
        assert my_sum(1,5,4) == 10
        assert my_sum(1,6.0,-4) == 3
        assert my_sum(1,2,3,4,5,6,7,8,9) == 45

    def test_my_concatenate(self):
        assert my_concatenate(prenom='Jhonatan', nom='Caldeira') == 'Jhonatan Caldeira'
        assert my_concatenate(prenom='éèÉÉÈÈÊõç', nom='éèÉÉÈÈÊõç') == 'éèÉÉÈÈÊõç éèÉÉÈÈÊõç'


if __name__ == '__main__':
    TestMyModule().test_my_sum()
    TestMyModule().test_my_concatenate()