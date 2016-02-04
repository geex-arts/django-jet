from django.test import TestCase
import pickle
from jet.ordered_set import OrderedSet


class OrderedSetTestCase(TestCase):
    def test_pickle(self):
        set1 = OrderedSet('abracadabra')
        roundtrip = pickle.loads(pickle.dumps(set1))
        self.assertEqual(roundtrip, set1)

    def test_empty_pickle(self):
        empty_oset = OrderedSet()
        empty_roundtrip = pickle.loads(pickle.dumps(empty_oset))
        self.assertEqual(empty_roundtrip, empty_oset)

    def test_order(self):
        set1 = OrderedSet('abracadabra')
        self.assertEqual(len(set1), 5)
        self.assertEqual(set1, OrderedSet(['a', 'b', 'r', 'c', 'd']))
        self.assertEqual(list(reversed(set1)), ['d', 'c', 'r', 'b', 'a'])

    def test_binary_operations(self):
        set1 = OrderedSet('abracadabra')
        set2 = OrderedSet('simsalabim')

        self.assertNotEqual(set1, set2)
        self.assertEqual(set1 & set2, OrderedSet(['a', 'b']))
        self.assertEqual(set1 | set2, OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l']))
        self.assertEqual(set1 - set2, OrderedSet(['r', 'c', 'd']))

    def test_remove(self):
        set1 = OrderedSet('abracadabra')

        set1.remove('a')
        set1.remove('b')

        self.assertEqual(set1, OrderedSet('rcd'))
        self.assertNotIn('a', set1)
        self.assertNotIn('b', set1)
        self.assertIn('r', set1)

        set1.discard('a')
        set1.discard('a')

    def test_remove_error(self):
        set1 = OrderedSet('abracadabra')
        try:
            set1.remove('z')
        except KeyError:
            pass

    def test_clear(self):
        set1 = OrderedSet('abracadabra')
        set1.clear()

        self.assertEqual(len(set1), 0)
        self.assertEqual(set1, OrderedSet())

    def test_pop(self):
        set1 = OrderedSet('ab')
        elem = set1.pop()

        self.assertEqual(elem, 'b')
        elem = set1.pop()

        self.assertEqual(elem, 'a')
        self.assertRaises(KeyError, set1.pop)
