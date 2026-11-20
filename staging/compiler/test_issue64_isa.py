"""Issue #64: new instruction-set architecture identity and independent RV32I checks."""
import re
import unittest
from pathlib import Path
from build import expand_static_transclusions

ROOT=Path(__file__).resolve().parents[2]
NAME="Instruction set architecture"
MAIN=ROOT/"Main"
NS={"Category","Template","Property","Help","BITwiki","Concept","Portal"}


def read(suffix=""):
    return (MAIN/(NAME+suffix+".mediawiki")).read_text(encoding="utf-8")


class InstructionSetArchitectureTests(unittest.TestCase):
    def test_depth_identity_and_transclusion(self):
        core,simple,technical=read(),read("/Simple"),read("/Technical")
        self.assertEqual(core.count("{{Knowledge object"),1)
        self.assertIn("|entity_type=Concept",core)
        self.assertIn("|domain=Computer science, Engineering",core)
        self.assertIn("{{#ask:",core)
        self.assertIn("{{:"+NAME+"/Simple}}",core)
        self.assertEqual(simple.count("<onlyinclude>"),1)
        self.assertEqual(simple.count("</onlyinclude>"),1)
        for body,depth in ((core,"Core"),(simple,"Simple"),(technical,"Technical")):
            self.assertIn("{{Reading depth|base="+NAME+"|current="+depth+"}}",body)
            self.assertIn("<references/>",body)
        self.assertNotIn("{{Knowledge object",simple+technical)
        self.assertNotIn("[[Related to::",simple+technical)
        expanded=expand_static_transclusions(core,NAME,{NAME+"/Simple":simple})
        self.assertIn("'''instruction set architecture'''",expanded)
        self.assertNotIn("current=Simple",expanded)
        self.assertGreater(len(simple.split()),400)
        self.assertGreater(len(technical.split()),1200)

    def test_source_citations_math_and_links(self):
        for name,body in (("core",read()),("simple",read("/Simple")),("technical",read("/Technical"))):
            with self.subTest(name=name):
                refs=re.findall(r'<ref name="([^"]+)">',body)
                uses=re.findall(r'<ref name="([^"]+)"\s*/>',body)
                self.assertEqual(len(refs),len(set(refs)))
                self.assertFalse(set(uses)-set(refs))
                self.assertEqual(len(re.findall(r"<math(?:\s+[^>]*)?>",body)),body.count("</math>"))
                for raw in re.findall(r"\[\[([^\]]+)\]\]",body):
                    target=raw.split("|")[0].split("#")[0].lstrip(":")
                    if "::" in target:
                        prop,target=target.split("::",1)
                        self.assertEqual(prop,"Related to")
                    part,sep,rest=target.partition(":")
                    filepath=(ROOT/part/(rest+".mediawiki") if sep and part in NS else MAIN/(target+".mediawiki"))
                    self.assertTrue(filepath.is_file(),f"{name}: missing link {target}")
        coredefs=set(re.findall(r'<ref name="([^"]+)">',read()))
        simplelead=read("/Simple").split("<onlyinclude>")[1].split("</onlyinclude>")[0]
        leaddefs=set(re.findall(r'<ref name="([^"]+)">',simplelead))
        self.assertFalse(coredefs&leaddefs)

    def test_independent_rv32i_encoding_and_semantics(self):
        funct7,rs2,rs1,funct3,rd,opcode=0,7,6,0,5,0x33
        widths=[7,5,5,3,5,7]
        self.assertEqual(sum(widths),32)
        word=(funct7<<25)|(rs2<<20)|(rs1<<15)|(funct3<<12)|(rd<<7)|opcode
        self.assertEqual(word,0x007302B3)
        self.assertEqual((word>>7)&31,5)
        self.assertEqual((word>>15)&31,6)
        self.assertEqual((word>>20)&31,7)
        self.assertEqual((word>>12)&7,0)
        self.assertEqual((word>>25)&127,0)
        self.assertEqual(word&127,0x33)
        self.assertEqual((0xFFFFFFFF+2)%(1<<32),1)
        tech=read("/Technical")
        for marker in ("0x007302B3","0xFFFFFFFF","20260120","RVWMO"):
            self.assertIn(marker,tech)


if __name__=="__main__":
    unittest.main(verbosity=2)
