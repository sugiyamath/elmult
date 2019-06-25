
# VoxEL benchmark dataset

This dataset has manual annotations with respect to Wikipedia over the same text written in five languages: German (de), English (en), Spanish (es), French (fr) and Italian (it). The dataset is composed of 15 annotated news articles (in each of the 5 languages; 75 articles in total) where there is the same number of sentences in each language, as well as the same set of annotations for each corresponding sentence in the different languages. Each language has a total of 94 sentences across the 15 articles. 

We propose two annotated versions of the dataset: a strict version that only annotates persons, organizations and places (per, for example, traditional NER/MUC definitions of an entity), and a relaxed version that includes a larger number of annotations (e.g., capturing entity mentions such as “inflation” that have a corresponding Wikipedia article). Both the relaxed and the strict versions have the same text in the same languages. The strict version has 204 annotations per language, while the relaxed version has 674 annotations per language.


This dataset include the following files:
a) strict version:
   - sVoxEL-de.ttl
   - sVoxEL-en.ttl
   - sVoxEL-es.ttl
   - sVoxEL-fr.ttl
   - sVoxEL-it.ttl

b) relaxed version:
   - rVoxEL-de.ttl
   - rVoxEL-en.ttl
   - rVoxEL-es.ttl
   - rVoxEL-fr.ttl
   - rVoxEL-it.ttl

The annotations were made with NIFity: a custom application developed to help manually annotate a text, whose output is directly expressed in the (NIF format)[http://persistence.uni-leipzig.org/nlp2rdf/]; this annotation tool is available at (github)[https://github.com/henryrosalesmendez/NIFify].


If you use VoxEL in a research work, we would ask you to reference the following paper that describes the dataset in detail:

Henry Rosales-Méndez, Aidan Hogan, Barbara Poblete. “VoxEL: A Benchmark Dataset for Multilingual Entity Linking”. International Semantic Web Conference (ISWC), Monterey, United States, 2018. [http://aidanhogan.com/docs/voxel-entity-linking.pdf]


License
-------

The VoxEL dataset is licensed under the Creative Commons Attribution 4.0 License (https://creativecommons.org/licenses/by/4.0/)



