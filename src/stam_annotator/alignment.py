class Pecha:

  def __init__(self, id_: str, base_path: Path):
    ...
    
  @property
  def stam_fn(self):
    return self.base_path / f"{self.id_}.opf" / "stam.json"

  def load():
    return AnnotationStore(self.stam_fn)
    
  @class_method
  def from_id(cls, id_: str) -> "Pecha":
    return cls(...)

  def get_annotation(self, id_: str) -> str:
    return str(AnnotationStore.annotation.id(id_))

class Alignment:
  def __init__(self, id_: str, base_path: Path)
    segment_source: {}
    segment_pairs: list[dict]
    self.pechas = {}
    self.load_alignment()

  @propertry
  def alignment_fn(self):
    return self.base_path / f"{self.id_}.opa" / "alignment.json"

  def load_alignment(self):
    data = json.load(self.alignment_fn)
    self.segment_source = data["segment_source"]
    self.segment_paris = data["segment_pairs"]

    # load pechas
    for id_ from self.segment_source.keys():
      self.pechas[id_] = Pecha.from_id(id_)
    
  def get_segment_pairs(self):
    for id_ in self.segment_pairs:
      yield self.get_segment_pair(id_)
      
  def get_segment_pair(self, id_) -> list[tuple[str, str]]:
    segment_pair = []
    for pecha_id, segment_id in self.segment_pairs[id_].items():
      segment_lang = self.segment_source[pecha_id]["lang"]
      segment_text = self.pecha[pecha_id].get_annotation(segment_id)
      segment_pair.append((segment_text, segment_lang))
    return segment_pair
  
  @classmethod
  from_id(cls, id_: str) -> "Alignment":
    """Load alignment from id"""
    alignment_repo_path = get_repo(org, id_, token)
    return cls(id_, base_path)

alignment = Alignment.from_id("A0B609189")
for segment_pair in alignment.get_segment_pairs():
  print(segment_pairs)

print(alignment.get_segment_pair("927f1b47e89d4a98b6f599c2633c2ba5"))
  
