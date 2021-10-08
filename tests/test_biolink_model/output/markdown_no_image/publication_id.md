
# Slot: id


Different kinds of publication subtypes will have different preferred identifiers (curies when feasible). Precedence of identifiers for scientific articles is as follows: PMID if available; DOI if not; actual alternate CURIE otherwise. Enclosing publications (i.e. referenced by 'published in' node property) such as books and journals, should have industry-standard identifier such as from ISBN and ISSN.

URI: [biolink:publication_id](https://w3id.org/biolink/vocab/publication_id)


## Domain and Range

[Publication](Publication.md) &#8594;  <sub>1..1</sub> [String](types/String.md)

## Parents

 *  is_a: [id](id.md)

## Children

 *  [book➞id](book_id.md)
 *  [serial➞id](serial_id.md)

## Used by

 * [Article](Article.md)
 * [BookChapter](BookChapter.md)
 * [Publication](Publication.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | translator_minimal |
| **Exact Mappings:** | | alliancegenome:primaryId |
|  | | gff3:ID |
|  | | gpi:DB_Object_ID |

