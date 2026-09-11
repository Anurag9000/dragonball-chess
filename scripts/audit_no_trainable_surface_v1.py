#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"artifacts"/"training_control"/"no_trainable_surface_v1.json"
TOKENS=(r"\.fit\s*\(",r"partial_fit\s*\(",r"\.backward\s*\(",r"torch\.optim",r"tensorflow",r"keras\.optim",r"optimizer\.step\s*\(",r"Trainer\s*\(")
def main()->int:
 files=[];findings=[]
 for path in sorted(ROOT.rglob("*")):
  if not path.is_file() or path.name=="run_all_training.py" or "vendor" in path.parts or ".training_control" in path.parts or "scripts" in path.relative_to(ROOT).parts: continue
  if path.suffix.lower() not in {".py",".js",".jsx",".ts",".tsx",".html"}: continue
  rel=path.relative_to(ROOT).as_posix();files.append(rel);text=path.read_text(encoding="utf-8",errors="replace")
  for token in TOKENS:
   if re.search(token,text,re.IGNORECASE):findings.append({"path":rel,"pattern":token})
 unresolved=[] if not findings else [{"type":"retained_training_primitives_detected","values":findings}]
 payload={"schema_version":1,"repository":"Anurag9000/dragonball-chess","classification":"static_browser_game_with_stockfish_inference" if not unresolved else "training_surface_detected","retained_code_files":files,"training_findings":findings,"unresolved":unresolved,"complete":not unresolved,"source_configuration_only":True,"training_executed_by_audit":False}
 OUTPUT.parent.mkdir(parents=True,exist_ok=True);tmp=OUTPUT.with_suffix(OUTPUT.suffix+".tmp");tmp.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8");tmp.replace(OUTPUT);print(json.dumps(payload,indent=2,sort_keys=True));return 0 if not unresolved else 2
if __name__=="__main__":raise SystemExit(main())
