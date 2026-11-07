# Elecrow デザインルール

確認日: 2026-11-07。

Regular Custom PCB、2層、1oz、板厚1.6mmに限定。穴径0.3mm、片側アニュラ0.15mmに整合する最小ビア外径0.6mmへ修正。資料のvia 0.25mmは穴径で、外径ではない。4層はアニュラ0.2mm以上、2ozは線幅/間隔0.25mm以上、板厚2mmは端面離隔1mm以上へ変更が必要。ICマスクダム0.25mmを設定。注文ページは取得時403のため、公開中の公式PDFを根拠とした。

[公式出典](https://www.elecrow.com/download/quote/PCB_Specification_FAQ.pdf)

単位はmm。製造限界と、既存の余裕を持たせた運用値を区別すること。

|KiCad設定|採用値|
|:--|--:|
|`min_clearance`|0.15|
|`min_connection`|0.0|
|`min_copper_edge_clearance`|0.7|
|`min_hole_clearance`|0.15|
|`min_hole_to_hole`|0.35|
|`min_microvia_diameter`|0.2|
|`min_microvia_drill`|0.1|
|`min_resolved_spokes`|2|
|`min_silk_clearance`|0.15|
|`min_text_height`|0.8|
|`min_text_thickness`|0.15|
|`min_through_hole_diameter`|0.3|
|`min_track_width`|0.15|
|`min_via_annular_width`|0.15|
|`min_via_diameter`|0.6|

カスタムルールは同名の `.kicad_dru` も一緒にコピーする。マスク設定は `.kicad_pcb` のsetupを使用する。THパッドのアニュラとビア外径・穴径は別の制約。マイクロビアの既存数値は製造対応の根拠ではなく、この2層テンプレートでは使用しない。

基板サイズ、スロット、面付け、Vカット、レジスト色/銅厚変更、同一ネット間隔は発注前に手動確認する。DRC合格だけで全製造条件を保証しない。P板.comのベタ～パッド0.5mmもゾーン個別設定を含め手動確認する。

変更前後の回路図・基板図と検証結果は `review-2026-11-07/` を参照。元データは空のテンプレートで部品・配線・外形がない。

検証: KiCad 10.0.7。寸法不足のトラック幅/ビア外径、および製造先別THアニュラ（PCBGOGOはNPTH穴径も）を検出し、余裕のある寸法では同じ違反が出ないことを確認。空の原本は外形がないため変更前後とも invalid_outline が1件あり、DRC全件合格とはしない。試験基板の外形は検証用でテンプレートに追加していない。

再実行: python verify_rules.py <kicad-cliのパス> <このフォルダのパス>。before/に変更前の回路図・基板図・設定、現在のフォルダに変更後データ、validation.jsonに試験結果を保存。実行時に変更前後のSVGも生成する。
