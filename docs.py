
class Docs:
    def __init__(self, service: object, document_id: str):
        self.document_id = document_id
        self.doc = service.documents().get(documentId=self.document_id).execute()
        self.title = self.doc.get('title')
        self.text = Docs.read_structural_elements(self.doc.get('body').get('content'))
        self.word_count = Docs.count_words(self.text)

    @staticmethod
    def read_paragraph_element(element: object):
        """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.

        Returns:
            The text from a paragraph element
        """

        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    @staticmethod
    def read_structural_elements(elements: list):
        """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: A list of Structural Elements.

        Returns:
            The entire document's text
        """

        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += Docs.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += Docs.read_structural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += Docs.read_structural_elements(toc.get('content'))
        return text

    @staticmethod
    def count_words(words: str):
        """Counts the number of words from text
        from Google Doc file.

        Args:
            words: Text from Google Docs file

        Returns:
             The word count
        """
        if len(words) == 0:
            return 0

        count = 0
        blocks = words.split("\n")

        for block in blocks:
            temp = block.rstrip()
            temp = temp.lstrip()
            count += len(temp.split())

        return count



