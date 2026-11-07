import pathlib,json,subprocess,shutil,sys
CLI=sys.argv[1]
folder=pathlib.Path(sys.argv[2]).resolve(); name=folder.name
review=folder/'review-2026-11-07'; review.mkdir(exist_ok=True)
def run(args):
 p=subprocess.run([CLI]+args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode: raise RuntimeError(p.stdout.decode(errors='replace'))
 return p.stdout.decode(errors='replace')
for state in ['before','after']:
 source=review/'before' if state=='before' else folder
 out=review/state; out.mkdir(exist_ok=True)
 run(['pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,B.SilkS,Edge.Cuts','--mode-single','-o',str(out/'pcb.svg'),str(source/f'{name}.kicad_pcb')])
 run(['sch','export','svg','-o',str(out/'schematic'),str(source/f'{name}.kicad_sch')])
 run(['pcb','drc','--severity-all','--format','json','-o',str(out/'drc.json'),str(source/f'{name}.kicad_pcb')])
test=review/'fixture'; test.mkdir(exist_ok=True)
shutil.copyfile(folder/f'{name}.kicad_pro',test/'test.kicad_pro')
shutil.copyfile(folder/f'{name}.kicad_dru',test/'test.kicad_dru')
base=(folder/f'{name}.kicad_pcb').read_text(encoding='utf-8')
def board(ring,width,via,npth):
 size=.6+ring*2
 return base[:base.rindex(')')]+f'''
 (gr_rect (start 0 0) (end 60 40) (stroke (width 0.05) (type default)) (fill none) (layer "Edge.Cuts"))
 (segment (start 5 5) (end 10 10) (width {width}) (layer "F.Cu") (net 0))
 (via (at 15 15) (size {via}) (drill 0.3) (layers "F.Cu" "B.Cu") (net 0))
 (footprint "Test" (layer "F.Cu") (at 25 20)
  (property "Reference" "TEST" (at 0 -2) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.15))))
  (pad "1" thru_hole circle (at 0 0) (size {size} {size}) (drill 0.6) (layers "*.Cu" "*.Mask"))
  (pad "" np_thru_hole circle (at 10 0) (size {npth} {npth}) (drill {npth}) (layers "*.Cu" "*.Mask"))
 )
)'''
results={}
for case,params in [('fail',(.05,.05,.4,.4)),('pass',(.3,.3,1,.8))]:
 (test/'test.kicad_pcb').write_text(board(*params),encoding='utf-8')
 run(['pcb','drc','--severity-all','--format','json','-o',str(test/f'{case}.json'),str(test/'test.kicad_pcb')])
 report=json.loads((test/f'{case}.json').read_text(encoding='utf-8'))
 results[case]=[{'type':v['type'],'description':v['description']} for v in report['violations']]
 types={v['type'] for v in report['violations']}
 expected={'track_width','via_diameter'}
 if name!='EasyEDA': expected.add('annular_width')
 if name=='PCBGOGO': expected.add('drill_out_of_range')
 if case=='fail': assert expected<=types, (name,expected,types)
 else: assert not (expected & types), (name,types)
(review/'validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(name,'PASS: undersize detected; compliant dimensions accepted')
