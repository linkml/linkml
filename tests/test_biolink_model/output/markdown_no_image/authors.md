
# Slot: authors


connects an publication to the list of authors who contributed to the publication. This property should be a comma-delimited list of author names. It is recommended that an author's name be formatted as "surname, firstname initial.".   Note that this property is a node annotation expressing the citation list of authorship which might typically otherwise be more completely documented in biolink:PublicationToProviderAssociation defined edges which point to full details about an author and possibly, some qualifiers which clarify the specific status of a given author in the publication.

URI: [biolink:authors](https://w3id.org/biolink/vocab/authors)


## Domain and Range

[Publication](Publication.md) &#8594;  <sub>0..\*</sub> [String](types/String.md)

## Parents

 *  is_a: [node property](node_property.md)

## Children


## Used by

 * [Article](Article.md)
 * [Book](Book.md)
 * [BookChapter](BookChapter.md)
 * [Publication](Publication.md)
 * [Serial](Serial.md)
