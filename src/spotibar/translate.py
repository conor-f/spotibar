from googletrans import Translator
import locale

class Translatore():
    __lang = 'en'
    translator = Translator()

    def __init__(self):
        locale.setlocale(locale.LC_ALL, "")
        message_language = locale.getlocale(locale.LC_MESSAGES)[0]
        if message_language is not None:
            self.set_lang(message_language[0:2])
        else:
            self.set_lang('en')

    def set_lang(self, lang):
        self.__lang = lang

    def translate(self, text):
        translation = self.translator.translate(text, dest=self.__lang)
        return translation.text # type: ignore