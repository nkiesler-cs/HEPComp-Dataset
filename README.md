# A Dataset of Higher Education Programming Competencies

This public version of the dataset goes hand in hand with the publication at ICANN 2023. 

The dataset should therefore be cited as follows:

Kiesler, N., Pfülb, B. (2023). Higher Education Programming Competencies: A Novel Dataset. In: Lazaros, I.,  Papaleonidas, A., Angelov, P., Jayne, C. (eds) Artificial Neural Networks and Machine Learning – ICANN 2023. ICANN 2023. Lecture Notes in Computer Science. Springer, Cham.

The dataset is licensed under the CC BY-NC-SA license.

## Dataset Structure

```javascript
{
  "<file id>":
  {
  "university": "<university>",
  "timestamp" : "<timestamp>",
  "<sentence ids in paragraph>":
    {
    "raw_text"          :"<raw paragraph text>",
    "<sentences' id[s]>":
      {
      "text_before"  : "<original sentence>",
      "<competency id>":
        {
        "text_transformed": "<transformed text>",
        "text_en": "<English translation>",
        "label":
          [ // one or more labels
            {
              <"label type">:
                {
                  "label_name": "<label name>",
                  "label_id"  : <label identifier>
                }
            },
          ]
        }
      }, // more competencies
    }, // more paragraphs with sentences
  }, // more files
  "label_lookup":
    {
    "<name>": id,
    id: "<name>",
    }
}
```

## Sub-Datasets for Linguistic Transformation and Classification Tasks

In order to continue working with the dataset, e.g., apply NLP or ML methods, a Python code base is provided that helps create two sub-datasets.
[dataset_converter.py](dataset_converter.py) creates two sub-datasets, one for the linguistic transformation and another one for classification tasks.
The linguistic transformation dataset contains: list of tuples with `<text before transformation>` and `<text after transformation>`.
The classification sub-dataset contains: list of tuples with `<text after transformation>` and  `<labels>`.
For more information, see [dataset_converter.py](dataset_converter.py).

## Original Module Handbooks

The original module handbooks/descriptions have been added to the folder [original module handbooks](original%20module%20handbooks).
