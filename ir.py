from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class IRInstruction:
    op: str
    dst: Optional[str] = None
    a: Optional[str] = None
    b: Optional[str] = None
    extra: Optional[str] = None
    source_line: int = 0

@dataclass
class IRFunction:
    name: str
    return_type: str
    params: List[str]
    instructions: List[IRInstruction] = field(default_factory=list)

@dataclass
class IRProgram:
    functions: List[IRFunction] = field(default_factory=list)

def generate_ir(program_ast, semantic_result) -> IRProgram:
    if not semantic_result.ok:
        raise ValueError("Cannot generate IR when semantic errors exist.")
    return IRProgram()

def dump_ir(ir_program: IRProgram):
    print("--- Student IR Dump ---")
    for fn in ir_program.functions:
        print(f"function {fn.return_type} ${fn.name}({', '.join(fn.params)}):")
        for instr in fn.instructions:
            if instr.op == "LABEL":
                print(f"  {instr.a}:")
            else:
                dst_str = f"{instr.dst} = " if instr.dst else ""
                args = [x for x in [instr.a, instr.b, instr.extra] if x is not None]
                print(f"    {dst_str}{instr.op} {', '.join(args)}")