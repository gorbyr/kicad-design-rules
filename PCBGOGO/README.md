# PCBGOGO デザインルール

確認日: 2026-11-07。

FR-4、2層、1oz、板厚1.6mm、緑レジストを対象。完成穴径0.2mmとアニュラ0.13mmから最小ビア外径0.46mmへ修正。線幅/間隔0.127mmは既存の余裕を維持（外層限界3mil、内層4mil）。NPTHは同じ表に0.3と0.5mmが併記されるため安全側0.5mm。文字高さも0.75mmの表記と0.8mm未満を避ける注記を踏まえ0.8mm。マスク拡張0.05mm、緑のブリッジ0.1mm。緑以外は0.15mmへ変更。板厚2mmでは穴0.3mm以上、2.4mmでは0.4mm以上。穴間0.25mm、穴～銅0.2mm、端面0.4mmは既存値を維持。

[公式出典](https://www.pcbgogo.com/capabilities/fr-4-pcb-manufacturing.html)

単位はmm。製造限界と、既存の余裕を持たせた運用値を区別すること。

|KiCad設定|採用値|
|:--|--:|
|`min_clearance`|0.127|
|`min_connection`|0.0|
|`min_copper_edge_clearance`|0.4|
|`min_hole_clearance`|0.2|
|`min_hole_to_hole`|0.25|
|`min_microvia_diameter`|0.2|
|`min_microvia_drill`|0.1|
|`min_resolved_spokes`|2|
|`min_silk_clearance`|0.1|
|`min_text_height`|0.8|
|`min_text_thickness`|0.15|
|`min_through_hole_diameter`|0.2|
|`min_track_width`|0.127|
|`min_via_annular_width`|0.13|
|`min_via_diameter`|0.46|

カスタムルールは同名の `.kicad_dru` も一緒にコピーする。マスク設定は `.kicad_pcb` のsetupを使用する。THパッドのアニュラとビア外径・穴径は別の制約。マイクロビアの既存数値は製造対応の根拠ではなく、この2層テンプレートでは使用しない。

基板サイズ、スロット、面付け、Vカット、レジスト色/銅厚変更、同一ネット間隔は発注前に手動確認する。DRC合格だけで全製造条件を保証しない。P板.comのベタ～パッド0.5mmもゾーン個別設定を含め手動確認する。

変更前後の回路図・基板図と検証結果は `review-2026-11-07/` を参照。元データは空のテンプレートで部品・配線・外形がない。

検証: KiCad 10.0.7。寸法不足のトラック幅/ビア外径、および製造先別THアニュラ（PCBGOGOはNPTH穴径も）を検出し、余裕のある寸法では同じ違反が出ないことを確認。空の原本は外形がないため変更前後とも invalid_outline が1件あり、DRC全件合格とはしない。試験基板の外形は検証用でテンプレートに追加していない。

再実行: python verify_rules.py <kicad-cliのパス> <このフォルダのパス>。before/に変更前の回路図・基板図・設定、現在のフォルダに変更後データ、validation.jsonに試験結果を保存。実行時に変更前後のSVGも生成する。
