'''
Python Code to extract sub-datasets of the full competency dataset for either the translations or classifications tasks.

The translation sub-dataset contains: list of [<text before transformation>, <text after transformation>].
The classification sub-dataset contains: list of [<text after transformation>, [<label[s]>]].

Dependencies:
 * tested with python version 3.8.7,
 * module json (built-in)
 * the existence of the dataset file "competency_dataset.json" in the current working directory
'''
import json

label_selector = {
  'non_op'   : lambda x:         x ==      0,
  'process'  : lambda x:    10 < x <=     16,
  'knowledge': lambda x:   100 < x <=    104,
  'inductive': lambda x:  1000 < x <=   1077,
  'non_cog'  : lambda x: 10000 < x <= 100033,
}

def _write_file(data, filename):
  ''' Write sub-dataset as json file into the current working directory.

  @param data    : data which is stored as json string
  @param filename: output filename
  '''
  print('create', filename, 'with', len(data), 'entries')
  with open(filename, 'w', encoding='utf8') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)

def _depth_iterator(dataset, keys, max_depth, _current_depth=0):
  ''' Recursive depth generator returns elements depending on the recursion depth of the dataset.

  @param dataset       : dataset as dictionary
  @param keys          : list of keys or "*" (all keys) that should be extracted at the deepest recursion step
  @param max_depth     : the deepest resursion step where elements are extracted
  @param _current_depth: recursive parameter that indicates the current depth
  @return recursive generator
  '''
  if not isinstance(dataset, dict): return
  for _, v in dataset.items():
    if _current_depth == max_depth:
      if keys == '*': yield dataset
      else          : yield [ dataset[key] for key in keys ]
      break
    yield from _depth_iterator(v, keys, max_depth, _current_depth + 1)

def create_transformation(dataset):
  ''' Create a linguistically transformed dataset (file: transformed_dataset.json).

  The translation dataset contains a list of: [
    [0] a single sentence before the translation, e.g., "Die Studierenden koennen die Laufzeit von Algorithmen bewerten,
                                                         vergleichen und in die zugehoerigen Komplexitaetsklassen einordnen.",
    [1] a single or multiple sentences after the translation, e.g., "Die Studierenden koennen die Laufzeit von Algorithmen bewerten.
                                                                     Die Studierenden koennen die Laufzeit von Algorithmen vergleichen.
                                                                     Die Studierenden koennen die Laufzeit von Algorithmen in die
                                                                     zugehoerigen Komplexitaetsklassen einordnen."
  ], ...

  @param dataset: the full competency dataset
  '''
  transformed_dataset = list()
  for all_sentences in _depth_iterator(dataset, '*', 3):
    transformed_dataset += [[all_sentences.pop('text_before'), ' '.join([ sentence['text_transformed'] for sentence in all_sentences.values() ])]]
  _write_file(transformed_dataset, 'transformed_dataset.json')

def create_classification(dataset, include_labels=['non_op', 'process', 'knowledge', 'inductive', 'non_cog'], lang='DE'):
  ''' Create a classification dataset (file: classification_dataset.json).

  The classification dataset contains a list of: [
    [0] a single sentence after the translation (change parameter "lang" to get the English version), e.g.,
        "Die Studierenden erlernen die prinzipiellen Beschraenkungen heutiger Computer bei der Loesung von wichtigen Problemen.",
    [1] a list of labels (depending on the parameter "include_labels"), e.g., [103, 11, 1001],
  ]
  @param dataset       : the full competency dataset
  @param include_labels: defines which sentences with corresponding category are extracted:
    * "non_op"   : include all sentences that are categorized as "not operationalized"          (        label id ==      0)
    * "process"  : include all sentences that are categorized as "cognitive process dimensions" (   10 < label id <=     16)
    * "knowledge": include all sentences that are categorized in "knowledge dimensions"         (  100 < label id <=    104)
    * "inductive": include all sentences that are categorized in "inductive categories"         ( 1000 < label id <=   1077)
    * "non_cog"  : include all sentences that are categorized as "non-cognitive competency"     (10000 < label id <= 100033)
    See "label_lookup" table at the end of the full dataset file in order to see all assigned label names and label IDs.
    For example: In order to build a classifcation dataset only with "non operationalized" and "cognitive process dimensions" set
                 include_labels to ["non_op", "process"] (this step can reduce the number of elements in the sub-dataset)
  @param lang: if "EN" use the english version of sentences, else german
  '''
  classification_dataset = list()
  keys = ['text_en', 'label'] if lang == 'EN' else ['text_transformed', 'label']
  for text_transformed, label_list in _depth_iterator(dataset, keys, 4):
    labels = [ label
      for label in [[*label.values()][0]['label_id']
      for label in label_list] if any(lambda_(label)
      for lambda_ in [*map(label_selector.get, include_labels)])
      ]
    classification_dataset += [(text_transformed, labels)] if len(labels) > 0 else []
  _write_file(classification_dataset, 'classification_dataset.json')

if __name__ == '__main__':
  with open('competency_dataset.json', 'r', encoding="utf8") as fp:
    dataset = json.load(fp)
    dataset.pop('label_lookup')

  create_transformation(dataset)
  create_classification(dataset)

