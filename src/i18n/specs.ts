/**
 * The spec dictionary — every technical field's TR/EN label, unit and group.
 *
 * Turkish labels are the vocabulary live TR dealer sites already use, so a
 * buyer reads the same words here as everywhere else he has been shopping.
 * Values are stored unit-free in the content files and rendered through this
 * table, which is why one YAML file serves both locales.
 */

import type { Locale } from '../config/site';

export type SpecGroup =
  | 'print' | 'head' | 'mechanical' | 'cutting' | 'electrical' | 'software' | 'physical';

export const SPEC_GROUPS: Record<SpecGroup, Record<Locale, string>> = {
  print:      { tr: 'Baskı', en: 'Printing' },
  head:       { tr: 'Kafa & Mürekkep', en: 'Printhead & Ink' },
  mechanical: { tr: 'Mekanik', en: 'Mechanical' },
  cutting:    { tr: 'Kesim', en: 'Cutting' },
  electrical: { tr: 'Elektrik & Ortam', en: 'Power & Environment' },
  software:   { tr: 'Yazılım & Bağlantı', en: 'Software & Connectivity' },
  physical:   { tr: 'Fiziksel', en: 'Physical' },
};

/** Group render order on a spec table. */
export const GROUP_ORDER: SpecGroup[] = [
  'print', 'head', 'mechanical', 'cutting', 'electrical', 'software', 'physical',
];

interface SpecDef {
  tr: string;
  en: string;
  unit?: { tr: string; en: string };
  group: SpecGroup;
}

const U = (tr: string, en = tr) => ({ tr, en });

export const SPECS = {
  /* --- printing -------------------------------------------------------- */
  printArea:      { tr: 'Baskı Alanı', en: 'Print Area', unit: U('mm × mm'), group: 'print' },
  printWidth:     { tr: 'Baskı Genişliği', en: 'Print Width', unit: U('mm'), group: 'print' },
  mediaWidth:     { tr: 'Maks. Malzeme Genişliği', en: 'Max Media Width', unit: U('mm'), group: 'print' },
  mediaHeight:    { tr: 'Baskı Yüksekliği', en: 'Max Media Height', unit: U('mm'), group: 'print' },
  mediaThickness: { tr: 'Malzeme Kalınlığı', en: 'Media Thickness', unit: U('mm'), group: 'print' },
  mediaWeight:    { tr: 'Maks. Malzeme Ağırlığı', en: 'Max Media Weight', unit: U('kg/m²'), group: 'print' },
  rollWeight:     { tr: 'Maks. Rulo Ağırlığı', en: 'Max Roll Weight', unit: U('kg'), group: 'print' },
  resolution:     { tr: 'Baskı Çözünürlüğü', en: 'Print Resolution', unit: U('dpi'), group: 'print' },
  speedModes:     { tr: 'Baskı Hızı', en: 'Print Speed', unit: U('m²/sa', 'm²/h'), group: 'print' },
  passModes:      { tr: 'Baskı Modları', en: 'Print Modes', unit: U('geçiş', 'pass'), group: 'print' },
  dropSize:       { tr: 'Damla Hacmi', en: 'Drop Volume', unit: U('pL'), group: 'print' },

  /* --- printhead & ink -------------------------------------------------- */
  printHead:        { tr: 'Baskı Kafası', en: 'Print Head', group: 'head' },
  headCount:        { tr: 'Kafa Sayısı', en: 'Head Count', unit: U('adet', 'pcs'), group: 'head' },
  headOptions:      { tr: 'Kafa Seçenekleri', en: 'Printhead Options', group: 'head' },
  colors:           { tr: 'Renk Skalası', en: 'Ink Channels', group: 'head' },
  inkType:          { tr: 'Mürekkep Tipi', en: 'Ink Type', group: 'head' },
  inkSupply:        { tr: 'Mürekkep Besleme', en: 'Ink Supply', group: 'head' },
  inkCapacity:      { tr: 'Boya Kapasitesi', en: 'Ink Capacity', unit: U('ml'), group: 'head' },
  inkConsumption:   { tr: 'Boya Tüketimi', en: 'Ink Consumption', unit: U('ml/m²'), group: 'head' },
  whiteCirculation: { tr: 'Beyaz Mürekkep Sirkülasyonu', en: 'White Ink Circulation', group: 'head' },

  /* --- mechanical -------------------------------------------------------- */
  table:         { tr: 'Tabla', en: 'Table / Bed', group: 'mechanical' },
  vacuumZones:   { tr: 'Vakum Bölgesi', en: 'Vacuum Zones', unit: U('bölge', 'zones'), group: 'mechanical' },
  feed:          { tr: 'Malzeme Besleme Sistemi', en: 'Media Feed System', group: 'mechanical' },
  takeUp:        { tr: 'Sarma Sistemi', en: 'Take-up System', group: 'mechanical' },
  curing:        { tr: 'Kurutma / Kürleme', en: 'Curing / Drying', group: 'mechanical' },
  heaters:       { tr: 'Isıtıcı Sistemi', en: 'Heating System', group: 'mechanical' },
  heightSensor:  { tr: 'Yükseklik Sensörü', en: 'Media Height Sensor', group: 'mechanical' },
  antiCollision: { tr: 'Kafa Çarpışma Sensörü', en: 'Head Anti-Collision', group: 'mechanical' },
  capping:       { tr: 'Kafa Koruma / Cap Sistemi', en: 'Capping Station', group: 'mechanical' },
  cleaning:      { tr: 'Kafa Temizleme', en: 'Head Cleaning', group: 'mechanical' },

  /* --- cutting ----------------------------------------------------------- */
  cuttingArea:     { tr: 'Kesim Alanı', en: 'Cutting Area', unit: U('mm × mm'), group: 'cutting' },
  cuttingSpeed:    { tr: 'Maks. Kesim Hızı', en: 'Max Cutting Speed', unit: U('mm/s'), group: 'cutting' },
  cuttingForce:    { tr: 'Kesim Basıncı', en: 'Cutting Force', unit: U('gf'), group: 'cutting' },
  cuttingAccuracy: { tr: 'Kesim Hassasiyeti', en: 'Cutting Accuracy', unit: U('mm'), group: 'cutting' },
  cuttingTools:    { tr: 'Kesim Takımı', en: 'Tool Modules', group: 'cutting' },
  cutFormats:      { tr: 'Kesim Formatları', en: 'Cut File Formats', group: 'cutting' },
  cutMaterials:    { tr: 'Kesim Malzemeleri', en: 'Cuttable Materials', group: 'cutting' },

  /* --- power & environment ----------------------------------------------- */
  powerSupply:   { tr: 'Güç Kaynağı', en: 'Power Supply', group: 'electrical' },
  power:         { tr: 'Güç Tüketimi', en: 'Power Consumption', unit: U('kW'), group: 'electrical' },
  current:       { tr: 'Akım', en: 'Current', unit: U('A'), group: 'electrical' },
  compressedAir: { tr: 'Basınçlı Hava', en: 'Compressed Air', group: 'electrical' },
  environment:   { tr: 'Çalışma Ortamı', en: 'Operating Environment', unit: U('°C / % BN', '°C / %RH'), group: 'electrical' },
  tempGradient:  { tr: 'Sıcaklık Değişim Limiti', en: 'Max Temperature Gradient', unit: U('°C/sa', '°C/h'), group: 'electrical' },
  noise:         { tr: 'Gürültü Seviyesi', en: 'Acoustic Noise', unit: U('dB(A)'), group: 'electrical' },
  ventilation:   { tr: 'Havalandırma', en: 'Ventilation', group: 'electrical' },

  /* --- software ----------------------------------------------------------- */
  rip:         { tr: 'RIP Yazılımı', en: 'RIP Software', group: 'software' },
  fileFormats: { tr: 'Desteklenen Formatlar', en: 'Supported File Formats', group: 'software' },
  interface:   { tr: 'Bağlantı', en: 'Interface', group: 'software' },

  /* --- physical ------------------------------------------------------------ */
  dimensions:       { tr: 'Makine Ölçüleri', en: 'Dimensions (W × D × H)', unit: U('mm'), group: 'physical' },
  cratedDimensions: { tr: 'Paket Ölçüleri', en: 'Crated Dimensions', unit: U('mm'), group: 'physical' },
  weight:           { tr: 'Ağırlık', en: 'Weight', unit: U('kg'), group: 'physical' },
  floorArea:        { tr: 'Gerekli Alan', en: 'Required Floor Area', unit: U('m²'), group: 'physical' },
} as const satisfies Record<string, SpecDef>;

export type SpecKey = keyof typeof SPECS;

/* --- ink-specific labels -------------------------------------------------- */

export const INK_SPECS = {
  chemistry:         { tr: 'Kimya', en: 'Chemistry' },
  cureMethod:        { tr: 'Kürleme Yöntemi', en: 'Curing Method' },
  cureDose:          { tr: 'Kürleme Dozu', en: 'Cure Dose', unit: U('mJ/cm²') },
  cureIntensity:     { tr: 'Kürleme Şiddeti', en: 'Cure Intensity', unit: U('mW/cm²') },
  wavelength:        { tr: 'Dalga Boyu', en: 'Wavelength', unit: U('nm') },
  postCure:          { tr: 'Son Kürlenme Süresi', en: 'Post-Cure Time', unit: U('saat', 'h') },
  transferTemp:      { tr: 'Transfer Sıcaklığı', en: 'Transfer Temperature', unit: U('°C') },
  transferTime:      { tr: 'Transfer Süresi', en: 'Transfer Time', unit: U('s') },
  fixation:          { tr: 'Fiksaj', en: 'Fixation' },
  channels:          { tr: 'Renk Kanalları', en: 'Colour Channels' },
  packaging:         { tr: 'Ambalaj', en: 'Packaging' },
  printheads:        { tr: 'Uyumlu Baskı Kafaları', en: 'Compatible Printheads' },
  machines:          { tr: 'Doğrulanmış Makineler', en: 'Validated Equipment' },
  oemEquivalent:     { tr: 'OEM Eşdeğeri', en: 'OEM Equivalent' },
  chipIncluded:      { tr: 'Çip Dahil', en: 'Chip Included' },
  changeover:        { tr: 'Geçiş Sınıfı', en: 'Changeover Class' },
  shelfLife:         { tr: 'Raf Ömrü', en: 'Shelf Life', unit: U('ay', 'months') },
  storageTemp:       { tr: 'Depolama Sıcaklığı', en: 'Storage Temperature', unit: U('°C') },
  operatingTemp:     { tr: 'Çalışma Sıcaklığı', en: 'Operating Temperature', unit: U('°C') },
  outdoorDurability: { tr: 'Dış Mekân Dayanımı', en: 'Outdoor Durability', unit: U('ay', 'months') },
  substrates:        { tr: 'Uygulanabilir Yüzeyler', en: 'Substrates' },
  viscosity:         { tr: 'Viskozite', en: 'Viscosity', unit: U('cps') },
  surfaceTension:    { tr: 'Yüzey Gerilimi', en: 'Surface Tension', unit: U('din/cm', 'dyn/cm') },
  ph:                { tr: 'pH', en: 'pH' },
  particleSize:      { tr: 'Partikül Boyutu', en: 'Particle Size', unit: U('nm') },
  fastness:          { tr: 'Haslık', en: 'Fastness' },
  certifications:    { tr: 'Sertifikalar', en: 'Certifications' },
} as const satisfies Record<string, { tr: string; en: string; unit?: { tr: string; en: string } }>;

export type InkSpecKey = keyof typeof INK_SPECS;

/* --- shared vocabularies --------------------------------------------------- */

export const SUBSTRATES = {
  glass:     { tr: 'Cam', en: 'Glass' },
  wood:      { tr: 'Ahşap', en: 'Wood' },
  mdf:       { tr: 'MDF', en: 'MDF' },
  foamboard: { tr: 'Dekota', en: 'Foam PVC' },
  pvc:       { tr: 'PVC', en: 'PVC' },
  polycarb:  { tr: 'Polikarbon', en: 'Polycarbonate' },
  acrylic:   { tr: 'Pleksi', en: 'Acrylic' },
  alucomp:   { tr: 'Alüminyum Kompozit', en: 'Aluminium Composite' },
  photoblock:{ tr: 'Fotoblok', en: 'Foam Board' },
  canvas:    { tr: 'Kanvas', en: 'Canvas' },
  wallpaper: { tr: 'Duvar Kağıdı', en: 'Wallcovering' },
  vinyl:     { tr: 'Folyo', en: 'Vinyl' },
  banner:    { tr: 'Branda', en: 'Banner' },
  mesh:      { tr: 'Mesh', en: 'Mesh' },
  textile:   { tr: 'Tekstil', en: 'Textile' },
  metal:     { tr: 'Metal', en: 'Metal' },
  ceramic:   { tr: 'Seramik', en: 'Ceramic' },
  leather:   { tr: 'Deri', en: 'Leather' },
  paper:     { tr: 'Kağıt', en: 'Paper' },
  film:      { tr: 'PET Film', en: 'PET Film' },
} as const satisfies Record<string, { tr: string; en: string }>;

export type SubstrateKey = keyof typeof SUBSTRATES;

export const HEAD_BRANDS = {
  ricoh:    'Ricoh',
  konica:   'Konica Minolta',
  epson:    'Epson',
  kyocera:  'Kyocera',
  toshiba:  'Toshiba',
  starfire: 'Fujifilm Starfire',
} as const;

export type HeadBrand = keyof typeof HEAD_BRANDS;

/** Colour-channel codes → label + swatch. Cl (varnish) and W render as chips. */
export const CHANNELS = {
  C:   { tr: 'Camgöbeği', en: 'Cyan', hex: '#0081D2' },
  M:   { tr: 'Macenta', en: 'Magenta', hex: '#E30161' },
  Y:   { tr: 'Sarı', en: 'Yellow', hex: '#FFE305' },
  K:   { tr: 'Siyah', en: 'Black', hex: '#0B0B0C' },
  Lc:  { tr: 'Açık Camgöbeği', en: 'Light Cyan', hex: '#8FCDEC' },
  Lm:  { tr: 'Açık Macenta', en: 'Light Magenta', hex: '#F09AC0' },
  Lk:  { tr: 'Açık Siyah', en: 'Light Black', hex: '#8A8D91' },
  W:   { tr: 'Beyaz', en: 'White', hex: '#FFFFFF', outlined: true },
  Or:  { tr: 'Turuncu', en: 'Orange', hex: '#F26522' },
  Gr:  { tr: 'Yeşil', en: 'Green', hex: '#00A651' },
  Vt:  { tr: 'Mor', en: 'Violet', hex: '#6B3FA0' },
  Bl:  { tr: 'Mavi', en: 'Blue', hex: '#0047AB' },
  Cl:  { tr: 'Lak', en: 'Varnish', hex: '#E8E8E8', hatched: true },
  Pr:  { tr: 'Primer', en: 'Primer', hex: '#D8D2C4', hatched: true },
  FlP: { tr: 'Flüor Pembe', en: 'Fluor Pink', hex: '#FF3D8B' },
  FlY: { tr: 'Flüor Sarı', en: 'Fluor Yellow', hex: '#E8FF3D' },
  FlB: { tr: 'Flüor Mavi', en: 'Fluor Blue', hex: '#3DBEFF' },
  FlG: { tr: 'Flüor Yeşil', en: 'Fluor Green', hex: '#3DFF87' },
} as const satisfies Record<string, {
  tr: string; en: string; hex: string; outlined?: boolean; hatched?: boolean;
}>;

export type ChannelCode = keyof typeof CHANNELS;

/* --- lookups ---------------------------------------------------------------- */

export function specLabel(key: SpecKey, locale: Locale): string {
  return SPECS[key][locale];
}

export function specUnit(key: SpecKey, locale: Locale): string | undefined {
  const def = SPECS[key] as SpecDef;
  return def.unit?.[locale];
}

export function specGroup(key: SpecKey): SpecGroup {
  return SPECS[key].group;
}

export function substrateLabel(key: SubstrateKey, locale: Locale): string {
  return SUBSTRATES[key][locale];
}

export function channelLabel(code: ChannelCode, locale: Locale): string {
  return CHANNELS[code][locale];
}
