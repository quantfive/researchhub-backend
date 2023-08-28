from citation.csl_constants import (
    ARTICLE,
    ARTICLE_JOURNAL,
    ARTICLE_MAGAZINE,
    ARTICLE_NEWSPAPER,
    BROADCAST,
    CHAPTER,
    ENTRY_DICTIONARY,
    ENTRY_ENCYCLOPEDIA,
    GRAPHIC,
    LEGAL_CASE,
    LEGISLATION,
    MOTION_PICTURE,
    PAPER_CONFERENCE,
    PERSONAL_COMMUNICATION,
    POST,
    POST_WEBLOG,
    SONG,
    SPEECH,
)

ARTWORK = "ARTWORK"
AUDIO_RECORDING = "AUDIO_RECORDING"
BILL = "BILL"
BLOG_POST = "BLOG_POST"
BOOK = "BOOK"
BOOK_SECTION = "BOOK_SECTION"
CASE = "CASE"
CONFERENCE_PAPER = "CONFERENCE_PAPER"
DICTIONARY_ENTRY = "DICTIONARY_ENTRY"
DOCUMENT = "DOCUMENT"
EMAIL = "EMAIL"
ENCYCLOPEDIA_ARTICLE = "ENCYCLOPEDIA_ARTICLE"
FILM = "FILM"
FORUM_POST = "FORUM_POST"
HEARING = "HEARING"
INSTANT_MESSAGE = "INSTANT_MESSAGE"
INTERVIEW = "INTERVIEW"
JOURNAL_ARTICLE = "JOURNAL_ARTICLE"
LETTER = "LETTER"
MAGAZINE_ARTICLE = "MAGAZINE_ARTICLE"
MANUSCRIPT = "MANUSCRIPT"
MAP = "MAP"
NEWSPAPER_ARTICLE = "NEWSPAPER_ARTICLE"
PATENT = "PATENT"
PODCAST = "PODCAST"
PREPRINT = "PREPRINT"
PRESENTATION = "PRESENTATION"
RADIO_BROADCAST = "RADIO_BROADCAST"
REPORT = "REPORT"
SOFTWARE = "SOFTWARE"
STATUTE = "STATUTE"
THESIS = "THESIS"
TV_BROADCAST = "TV_BROADCAST"
VIDEO_RECORDING = "VIDEO_RECORDING"
WEBPAGE = "WEBPAGE"

ZOTERO_TO_CSL_MAPPING = {
    ARTWORK: GRAPHIC,
    AUDIO_RECORDING: SONG,
    BILL: BILL,
    BLOG_POST: POST_WEBLOG,
    BOOK: BOOK,
    BOOK_SECTION: CHAPTER,
    CASE: LEGAL_CASE,
    CONFERENCE_PAPER: PAPER_CONFERENCE,
    DICTIONARY_ENTRY: ENTRY_DICTIONARY,
    DOCUMENT: DOCUMENT,
    EMAIL: PERSONAL_COMMUNICATION,
    ENCYCLOPEDIA_ARTICLE: ENTRY_ENCYCLOPEDIA,
    FILM: MOTION_PICTURE,
    FORUM_POST: POST,
    HEARING: HEARING,
    INSTANT_MESSAGE: PERSONAL_COMMUNICATION,
    INTERVIEW: INTERVIEW,
    JOURNAL_ARTICLE: ARTICLE_JOURNAL,
    LETTER: PERSONAL_COMMUNICATION,
    MAGAZINE_ARTICLE: ARTICLE_MAGAZINE,
    MANUSCRIPT: MANUSCRIPT,
    MAP: MAP,
    NEWSPAPER_ARTICLE: ARTICLE_NEWSPAPER,
    PATENT: PATENT,
    PODCAST: BROADCAST,
    PREPRINT: ARTICLE,
    PRESENTATION: SPEECH,
    RADIO_BROADCAST: BROADCAST,
    REPORT: REPORT,
    SOFTWARE: SOFTWARE,
    STATUTE: LEGISLATION,
    THESIS: THESIS,
    TV_BROADCAST: BROADCAST,
    VIDEO_RECORDING: MOTION_PICTURE,
    WEBPAGE: WEBPAGE,
}

CSL_TO_ZOTERO_MAPPING = {value: key for key, value in ZOTERO_TO_CSL_MAPPING.items()}

CITATION_TYPE_CHOICES = (
    (ARTWORK, ARTWORK),
    (AUDIO_RECORDING, AUDIO_RECORDING),
    (BILL, BILL),
    (BLOG_POST, BLOG_POST),
    (BOOK, BOOK),
    (BOOK_SECTION, BOOK_SECTION),
    (CASE, CASE),
    (CONFERENCE_PAPER, CONFERENCE_PAPER),
    (DICTIONARY_ENTRY, DICTIONARY_ENTRY),
    (DOCUMENT, DOCUMENT),
    (EMAIL, EMAIL),
    (ENCYCLOPEDIA_ARTICLE, ENCYCLOPEDIA_ARTICLE),
    (FILM, FILM),
    (FORUM_POST, FORUM_POST),
    (HEARING, HEARING),
    (INSTANT_MESSAGE, INSTANT_MESSAGE),
    (INTERVIEW, INTERVIEW),
    (JOURNAL_ARTICLE, JOURNAL_ARTICLE),
    (LETTER, LETTER),
    (MAGAZINE_ARTICLE, MAGAZINE_ARTICLE),
    (MANUSCRIPT, MANUSCRIPT),
    (MAP, MAP),
    (NEWSPAPER_ARTICLE, NEWSPAPER_ARTICLE),
    (PATENT, PATENT),
    (PODCAST, PODCAST),
    (PREPRINT, PREPRINT),
    (PRESENTATION, PRESENTATION),
    (RADIO_BROADCAST, RADIO_BROADCAST),
    (REPORT, REPORT),
    (SOFTWARE, SOFTWARE),
    (STATUTE, STATUTE),
    (THESIS, THESIS),
    (TV_BROADCAST, TV_BROADCAST),
    (VIDEO_RECORDING, VIDEO_RECORDING),
    (WEBPAGE, WEBPAGE),
)


CITATION_TYPE_FIELDS = {
    JOURNAL_ARTICLE: [
        "title",
        "abstract",
        "container-title",
        "volume",
        "issue",
        "page",
        "collection-title",
        "journalAbbreviation",
        "language",
        "DOI",
        "ISSN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    ARTWORK: [
        "title",
        "abstract",
        "medium",
        "dimensions",
        "language",
        "title-short",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "URL",
        "note",
    ],
    AUDIO_RECORDING: [
        "title",
        "abstract",
        "medium",
        "collection-title",
        "volume",
        "number-of-volumes",
        "publisher-place",
        "publisher",
        "dimensions",
        "language",
        "ISBN",
        "title-short",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "URL",
        "note",
    ],
    BILL: [
        "title",
        "abstract",
        "number",
        "container-title",
        "volume",
        "section",
        "page",
        "authority",
        "chapter-number",
        "references",
        "language",
        "URL",
        "title-short",
        "note",
    ],
    BLOG_POST: [
        "title",
        "abstract",
        "container-title",
        "genre",
        "URL",
        "language",
        "title-short",
        "note",
    ],
    BOOK: [
        "title",
        "abstract",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "number-of-pages",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    BOOK_SECTION: [
        "title",
        "abstract",
        "container-title",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "page",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    CASE: [
        "title",
        "abstract",
        "authority",
        "number",
        "container-title",
        "volume",
        "page",
        "references",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    SOFTWARE: [
        "title",
        "abstract",
        "collection-title",
        "version",
        "medium",
        "publisher-place",
        "publisher",
        "genre",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    CONFERENCE_PAPER: [
        "title",
        "abstract",
        "container-title",
        "event-title",
        "publisher-place",
        "publisher",
        "volume",
        "page",
        "collection-title",
        "language",
        "DOI",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    DICTIONARY_ENTRY: [
        "title",
        "abstract",
        "container-title",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "page",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    DOCUMENT: [
        "title",
        "abstract",
        "publisher",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    EMAIL: [
        "title",
        "abstract",
        "title-short",
        "URL",
        "language",
        "license",
        "note",
    ],
    ENCYCLOPEDIA_ARTICLE: [
        "title",
        "abstract",
        "container-title",
        "collection-title",
        "collection-number",
        "volume",
        "number-of-volumes",
        "edition",
        "publisher-place",
        "publisher",
        "page",
        "ISBN",
        "title-short",
        "URL",
        "language",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    FILM: [
        "title",
        "abstract",
        "publisher",
        "genre",
        "medium",
        "dimensions",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    FORUM_POST: [
        "title",
        "abstract",
        "container-title",
        "genre",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    HEARING: [
        "title",
        "abstract",
        "section",
        "publisher-place",
        "publisher",
        "number-of-volumes",
        "number",
        "page",
        "authority",
        "chapter-number",
        "references",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    INSTANT_MESSAGE: [
        "title",
        "abstract",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    INTERVIEW: [
        "title",
        "abstract",
        "medium",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    LETTER: [
        "title",
        "abstract",
        "genre",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    MAGAZINE_ARTICLE: [
        "title",
        "abstract",
        "container-title",
        "volume",
        "issue",
        "page",
        "language",
        "ISSN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    MANUSCRIPT: [
        "title",
        "abstract",
        "genre",
        "publisher-place",
        "number-of-pages",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    MAP: [
        "title",
        "abstract",
        "genre",
        "scale",
        "collection-title",
        "edition",
        "publisher-place",
        "publisher",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    NEWSPAPER_ARTICLE: [
        "title",
        "abstract",
        "container-title",
        "publisher-place",
        "edition",
        "section",
        "page",
        "language",
        "title-short",
        "ISSN",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    PATENT: [
        "title",
        "abstract",
        "publisher-place",
        "authority",
        "number",
        "page",
        "call-number",
        "issue",
        "references",
        "status",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    PODCAST: [
        "title",
        "abstract",
        "collection-title",
        "number",
        "medium",
        "dimensions",
        "URL",
        "language",
        "title-short",
        "note",
    ],
    PREPRINT: [
        "title",
        "abstract",
        "genre",
        "publisher",
        "number",
        "publisher-place",
        "collection-title",
        "collection-number",
        "DOI",
        "URL",
        "archive",
        "archive_location",
        "title-short",
        "language",
        "source",
        "call-number",
        "note",
    ],
    PRESENTATION: [
        "title",
        "abstract",
        "genre",
        "publisher-place",
        "event-title",
        "URL",
        "language",
        "title-short",
        "note",
    ],
    RADIO_BROADCAST: [
        "title",
        "abstract",
        "container-title",
        "number",
        "medium",
        "publisher-place",
        "publisher",
        "dimensions",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    REPORT: [
        "title",
        "abstract",
        "number",
        "genre",
        "collection-title",
        "publisher-place",
        "publisher",
        "page",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    STATUTE: [
        "title",
        "abstract",
        "container-title",
        "volume",
        "number",
        "page",
        "section",
        "chapter-number",
        "references",
        "language",
        "title-short",
        "URL",
        "note",
    ],
    THESIS: [
        "title",
        "abstract",
        "genre",
        "publisher",
        "publisher-place",
        "number-of-pages",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    TV_BROADCAST: [
        "title",
        "abstract",
        "container-title",
        "number",
        "medium",
        "publisher-place",
        "publisher",
        "dimensions",
        "language",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    VIDEO_RECORDING: [
        "title",
        "abstract",
        "medium",
        "collection-title",
        "volume",
        "number-of-volumes",
        "publisher-place",
        "publisher",
        "dimensions",
        "language",
        "ISBN",
        "title-short",
        "URL",
        "archive",
        "archive_location",
        "source",
        "call-number",
        "note",
    ],
    WEBPAGE: [
        "title",
        "abstract",
        "container-title",
        "genre",
        "title-short",
        "URL",
        "language",
        "note",
    ],
}
