from bad_words.words import BAD_WORDS
from telegram import Message
from telegram.ext.filters import Text


class BadText(Text):
    """Class for filtering bad text."""
    def filter(self, message: Message) -> bool:
        """
        Filter the message for bad text.
        :param message: The message to be filtered.
        :type message: Message
        :return: True if the message contains bad words, False otherwise.
        :rtype: bool
        """
        if super(BadText, self).filter(message):
            return any(word in BAD_WORDS for word in message.text.split())
        return False


BAD_TEXT = BadText()
