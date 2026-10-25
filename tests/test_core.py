"""Tests for the UI-independent core shared by both editions.

Run from the repository root:

    python -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import ascii_data, bases, ipv4  # noqa: E402


class BaseConversionTests(unittest.TestCase):
    def test_parse_prefixes_and_separators(self):
        self.assertEqual(bases.parse_number("0xFF", 16), (255, None))
        self.assertEqual(bases.parse_number("1111 1111", 2), (255, None))
        self.assertEqual(bases.parse_number("1_000", 10), (1000, None))
        self.assertEqual(bases.parse_number("0o755", 8), (493, None))
        self.assertEqual(bases.parse_number("-1010", 2), (-10, None))
        self.assertEqual(bases.parse_number("", 10), (None, None))

    def test_parse_errors_are_structured(self):
        value, err = bases.parse_number("2", 2)
        self.assertIsNone(value)
        self.assertEqual(err[0], "badchar")
        self.assertEqual(err[1]["c"], "2")
        self.assertEqual(bases.parse_number("0x", 16)[1][0], "neednum")
        self.assertEqual(bases.parse_number("1" * (bases.MAX_INPUT + 1), 10)[1][0],
                         "toolong")

    def test_format(self):
        self.assertEqual(bases.format_value(255, 2), "1111 1111")
        self.assertEqual(bases.format_value(-10, 2), "-1010")
        self.assertEqual(bases.format_value(255, 8), "377")
        self.assertEqual(bases.format_value(255, 10), "255")
        self.assertEqual(bases.format_value(255, 16), "FF")


class AsciiTests(unittest.TestCase):
    def test_table_shape(self):
        self.assertEqual(len(ascii_data.ADATA), 128)
        self.assertEqual(ascii_data.ADATA[65][0], 65)

    def test_column_prefix_search(self):
        rows = ascii_data.search(ascii_data.ADATA, "0x41")
        self.assertEqual([row[0] for row in rows], [65])
        rows = ascii_data.search(ascii_data.ADATA, "0b01000001")
        self.assertEqual([row[0] for row in rows], [65])

    def test_description_search(self):
        self.assertEqual([row[0] for row in
                          ascii_data.search(ascii_data.ADATA, "Line Feed")], [10])
        self.assertEqual([row[0] for row in
                          ascii_data.search(ascii_data.ADATA, "换行")], [10])


class Ipv4Tests(unittest.TestCase):
    def test_cidr_and_subnet(self):
        result, err = ipv4.parse("192.168.1.10/24")
        self.assertIsNone(err)
        self.assertEqual(result.dotted, "192.168.1.10")
        subnet = result.subnet()
        self.assertEqual(ipv4.dotted(subnet.mask), "255.255.255.0")
        self.assertEqual(ipv4.dotted(subnet.network), "192.168.1.0")
        self.assertEqual(ipv4.dotted(subnet.broadcast), "192.168.1.255")
        self.assertEqual((ipv4.dotted(subnet.first), ipv4.dotted(subnet.last)),
                         ("192.168.1.1", "192.168.1.254"))
        self.assertEqual(subnet.hosts, 254)
        self.assertEqual(result.scope, "ipScopePrivate")

    def test_point_to_point_and_host_route(self):
        result, _ = ipv4.parse("10.0.0.1/31")
        subnet = result.subnet()
        self.assertEqual(subnet.note, "rfc3021")
        self.assertEqual(subnet.hosts, 2)
        result, _ = ipv4.parse("10.0.0.1/32")
        subnet = result.subnet()
        self.assertEqual(subnet.hosts, 1)
        self.assertEqual(subnet.first, subnet.last)

    def test_dotted_mask_and_alternate_forms(self):
        for text in ("192.168.1.10/255.255.255.0",
                     "192.168.1.10 255.255.255.0"):
            result, err = ipv4.parse(text)
            self.assertIsNone(err, text)
            self.assertEqual(result.prefix, 24)
        result, err = ipv4.parse("11000000.10101000.00000001.00001010")
        self.assertIsNone(err)
        self.assertEqual(result.dotted, "192.168.1.10")

    def test_invalid_inputs(self):
        for text, code in (("192.168.1.999", "seg_range"),
                           ("192.168.1", "addr"),
                           ("192.168.1.10/33", "prefix"),
                           ("1.2.3.4/255.0.255.0", "mask")):
            result, err = ipv4.parse(text)
            self.assertIsNone(result, text)
            self.assertEqual(err[0], code, text)


if __name__ == "__main__":
    unittest.main()
