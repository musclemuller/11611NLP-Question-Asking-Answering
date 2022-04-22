import spacy
import stanza
import logging
# import neuralcoref

logger = logging.getLogger('stanza')
logger.disabled = True
spacy_nlp = spacy.load('en_core_web_lg')
# hugging face's model https://github.com/huggingface/neuralcoref
# pip install neuralcoref --no-binary neuralcoref <- in terminal to download
# neuralcoref.add_to_pipe(spacy_nlp)

stanza_nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,constituency,lemma,depparse,ner', verbose=False)
